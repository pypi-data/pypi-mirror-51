import logging
import time

import tqdm

import torch
from torch import optim
from torch.nn.utils import clip_grad_norm_

logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)


import pie.trainer as trainer

from .utils import constants


class EarlyStopException(trainer.EarlyStopException):
    def __init__(self, task, loss, state_dict):
        self.task = task
        self.loss = loss
        self.best_state_dict = state_dict


class Trainer(trainer.Trainer):
    """
    Trainer

    Settings
    ========
    optim
    lr
    clip_norm
    weights
    report_freq
    checks_per_epoch
    """
    def __init__(self, settings, model, dataset, num_instances):
        self.verbose = settings.verbose
        self.dataset = dataset
        self.model = model
        self.optimizer = getattr(optim, settings.optimizer)(
            model.parameters(), lr=settings.lr)
        self.clip_norm = settings.clip_norm

        self.report_freq = settings.report_freq
        self.num_batches = num_instances // dataset.batch_size
        if settings.checks_per_epoch == 1:
            self.check_freq = self.num_batches - 1  # check after last batch
        elif settings.checks_per_epoch > self.num_batches:
            self.check_freq = 1  # check after each batch
        elif settings.checks_per_epoch > 1:
            self.check_freq = self.num_batches // settings.checks_per_epoch  # check just
        else:
            self.check_freq = 0  # no checks

        tasks = {
            constants.scheduler_task_name: {
                "target": True,
                "weight": 1.
            }
        }

        self.task_scheduler = trainer.TaskScheduler(
            # task schedule
            tasks, settings.schedule.get("patience", 2), settings.factor, settings.schedule.get("threshold", 0.001),
            settings.min_weight,
            # lr schedule
            optimizer=self.optimizer,
            lr_factor=settings.lr_factor, lr_patience=settings.lr_patience)

        if settings.verbose:
            print()
            print("Evaluation check every {}/{} batches".format(
                self.check_freq, self.num_batches))
            print()
            print("::: Task schedules :::")
            print()
            print(self.task_scheduler)
            print()

    def weight_loss(self, loss):
        """ In original pie, multiple task and weight, here, None"""
        return loss

    def evaluate(self, dataset):
        """
        Evaluate objective on held-out data
        """
        losses, total_batches = 0., 0

        for batch in tqdm.tqdm(dataset.batch_generator()):
            total_batches += 1
            losses += self.model.loss(batch).item()

        return losses / total_batches

    def run_check(self, devset):
        """
        Monitor dev loss and eventually early-stop training
        """
        print()
        print("Evaluating model on dev set...")
        print()

        self.model.eval()

        with torch.no_grad():
            dev_loss = self.evaluate(devset)
            print()
            print("::: Dev losses :::")
            print()
            print('Disambiguation: {:.3f}'.format(dev_loss))
            print()
            scorer = self.model.evaluate(devset, self.dataset)
            scorer.print_summary()

        self.model.train()

        dev_scores = {
            constants.scheduler_task_name: scorer.get_scores()['all']['accuracy']
        }
        self.task_scheduler.step(dev_scores, self.model)

        if self.verbose:
            print(self.task_scheduler)
            print()

        return dev_scores

    def train_epoch(self, devset, epoch):
        rep_loss = 0.
        rep_batches = 0
        rep_items, rep_start = 0, time.time()
        scores = None

        for b, batch in enumerate(self.dataset.batch_generator()):
            # get loss
            loss = self.model.loss(batch)

            if not loss:
                raise ValueError("Got empty loss, no tasks defined?")

            # optimize
            self.optimizer.zero_grad()
            self.weight_loss(loss).backward()
            if self.clip_norm > 0:
                clip_grad_norm_(self.model.parameters(), self.clip_norm)
            self.optimizer.step()

            # accumulate
            rep_items += type(self.dataset).get_nelement(batch)
            rep_batches += 1
            rep_loss += loss.item()

            # report
            if self.report_freq and b > 0 and b % self.report_freq == 0:
                rep = 'Disambiguation:{:.3f}  '.format(rep_loss / rep_batches)

                logging.info("Batch [{}/{}] || {} || {:.0f} w/s".format(
                    b, self.num_batches, rep, rep_items / (time.time() - rep_start)))
                rep_loss = 0.
                rep_batches = 0
                rep_items, rep_start = 0, time.time()

            if self.check_freq > 0 and b > 0 and b % self.check_freq == 0:
                if devset is not None:
                    scores = self.run_check(devset)

        return scores

    def train_epochs(self, epochs, devset=None):
        """
        Train the model for a number of epochs
        """
        start = time.time()
        scores = None

        try:
            for epoch in range(1, epochs + 1):
                # train epoch
                epoch_start = time.time()
                logging.info("Starting epoch [{}]".format(epoch))
                self.train_epoch(devset, epoch)
                epoch_total = time.time() - epoch_start
                logging.info("Finished epoch [{}] in [{:g}] secs".format(
                    epoch, epoch_total))

        except trainer.EarlyStopException as e:
            logging.info("Early stopping training: "
                         "task [{}] with best score {:.5f}".format(e.task, e.loss))

            self.model.load_state_dict(e.best_state_dict)
            scores = e.loss

        logging.info("Finished training in [{:g}]".format(time.time() - start))

        # will be None if no dev test was provided or the model failed to converge
        return scores
