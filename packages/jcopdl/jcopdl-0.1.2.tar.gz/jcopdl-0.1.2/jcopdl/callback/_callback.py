import os
import torch
import matplotlib.pyplot as plt
import numpy as np


class Callback:
    """
    Callback for common PyTorch Workflow:
    - Neat Checkpoint and Logs
    - Earl stopping
    - Runtime Plotting
    - Runtime Log and Reporting


    == Example Usage ==
    = Config Definition =
    class Config:
        input_size = 784
        hl1 = 256
        hl2 = 64
        output_size = 10
        dropout = 0.2

    = Using Callback =
    # Logging
    callback.log(train_cost, test_cost, train_score, test_score)

    # Checkpoint
    callback.save_checkpoint()

    # Runtime Plotting
    callback.cost_runtime_plotting()
    callback.score_runtime_plotting()

    # Early Stopping
    if callback.early_stopping(model):
        callback.cost_runtime_plotting()
        callback.score_runtime_plotting()
        break
    else:
        callback.next_epoch()


    == Arguments ==
    model: torch.nn.Module
        A deep learning architecture using PyTorch nn.Module

    config: Config
        a config object containing the architecture parameters' that you would want to save

    init_epoch: int
        initial epoch

    save_every: int
        number of epoch to save a checkpoint

    early_stop_patience: int
        number of patience before executing early stopping

    plot_every: int
        number of epoch to perform runtime plotting

    outdir: string
        path of output directory to save the weights, configs, and logs
    """

    def __init__(self, model, config=None, save_every=50, early_stop_patience=5,
                 plot_every=20, outdir="model"):
        self.save_every = save_every
        self.early_stop_patience = early_stop_patience
        self.plot_every = plot_every
        self.outdir = outdir

        self.ckpt = Checkpoint(model, config)
        os.makedirs(self.outdir, exist_ok=True)

    def save_checkpoint(self):
        if self.ckpt.epoch % self.save_every == 0:
            self._save("checkpoint")

    def early_stopping(self, model, monitor='test_score'):
        stop = False
        if monitor == "train_cost":
            reference = self.ckpt.train_cost[-1]
            improve = reference < self.ckpt.best_cost
        elif monitor == "test_cost":
            reference = self.ckpt.test_cost[-1]
            improve = reference < self.ckpt.best_cost
        elif monitor == "train_score":
            reference = self.ckpt.train_score[-1]
            improve = reference > self.ckpt.best_score
        elif monitor == "test_score":
            reference = self.ckpt.test_score[-1]
            improve = reference > self.ckpt.best_score
        else:
            raise Exception('Only supports monitor={"train_cost", "test_cost", "train_score", "test_score"}')

        if improve:
            if monitor.endswith("_cost"):
                self.ckpt.best_cost = reference
            elif monitor.endswith("_score"):
                self.ckpt.best_score = reference
            self.ckpt.weights = model.state_dict()
            self.ckpt.early_stop = 0
        else:
            self.ckpt.early_stop += 1
            print(f"==> EarlyStop patience = {self.ckpt.early_stop}")

            if self.ckpt.early_stop >= self.early_stop_patience:
                best = self.ckpt.best_cost if monitor.endswith("_cost") else self.ckpt.best_score
                print(f'==> Execute Early Stopping at epoch: {self.ckpt.epoch} | Best {monitor}: {best:.4f}')
                self._save("best")
                print(f'==> Best model is saved at {self.outdir}')
                self.ckpt.epoch += 1
                stop = True
        self.ckpt.epoch += 1
        return stop

    def cost_runtime_plotting(self, scale="semilogy", figsize=(8, 5)):
        self._runtime_plotting(scale, figsize, mode="Cost")

    def score_runtime_plotting(self, scale="linear", figsize=(8, 5)):
        self._runtime_plotting(scale, figsize, mode="Score")

    def next_epoch(self):
        self.ckpt.epoch += 1

    def log(self, train_cost=None, test_cost=None, train_score=None, test_score=None):
        report = f'Epoch {self.ckpt.epoch:5}\n'
        if train_cost is not None:
            train_cost = train_cost.item() if type(train_cost) == torch.Tensor else train_cost
            self.ckpt.train_cost.append(train_cost)
            report += f'Train_cost  = {train_cost:.4f} | '
        if test_cost is not None:
            test_cost = test_cost.item() if type(test_cost) == torch.Tensor else test_cost
            self.ckpt.test_cost.append(test_cost)
            report += f'Test_cost  = {test_cost:.4f} |\n'
        if train_score is not None:
            train_score = train_score.item() if type(train_score) == torch.Tensor else train_score
            self.ckpt.train_score.append(train_score)
            report += f'Train_score = {train_score:.4f} | '
        if test_score is not None:
            test_score = test_score.item() if type(test_score) == torch.Tensor else test_score
            self.ckpt.test_score.append(test_score)
            report += f'Test_score = {test_score:.4f} |\n'
        print(report)

    def _runtime_plotting(self, scale, figsize, mode):
        plot_func = self._plot_func(scale)
        if self.ckpt.epoch % self.plot_every == 0:
            plt.figure(figsize=figsize)
            plt.ylabel(mode)
            plt.xlabel("Epoch")
            if mode == "Cost":
                plot_func(range(1, self.ckpt.epoch + 1), self.ckpt.train_cost, 'r-', label="Train")
                if self.ckpt.test_cost != []:
                    plot_func(range(1, self.ckpt.epoch + 1), self.ckpt.test_cost, 'b-', label="Test")
            elif mode == "Score":
                plot_func(range(1, self.ckpt.epoch + 1), self.ckpt.train_score, 'r-', label="Train")
                if self.ckpt.test_score != []:
                    plot_func(range(1, self.ckpt.epoch + 1), self.ckpt.test_score, 'b-', label="Test")
            plt.legend()
            plt.show();

    def _save(self, mode):
        # Save weights
        weights = self.ckpt.weights
        if mode == "checkpoint":
            torch.save(weights, f'{self.outdir}/weights_{self.ckpt.epoch}.pth')
        elif mode == "best":
            torch.save(weights, f'{self.outdir}/weights_best.pth')

            # Save config if exist
        if self.ckpt.config is not None:
            configs = self.ckpt.config
            torch.save(configs, f'{self.outdir}/configs.pth')

        # Save logs
        logs = self._parse_logs()
        torch.save(logs, f'{self.outdir}/logs.pth')

    def _parse_logs(self):
        logs = {
            "train_cost": self.ckpt.train_cost,
            "train_score": self.ckpt.train_score,
            "final_epoch": self.ckpt.epoch
        }
        if self.ckpt.best_cost < np.inf:
            logs["best_cost"] = self.ckpt.best_cost
        if self.ckpt.best_score > 0:
            logs["best_score"] = self.ckpt.best_score
        if self.ckpt.test_cost != []:
            logs["test_cost"] = self.ckpt.test_cost
        if self.ckpt.test_score != []:
            logs["test_score"] = self.ckpt.test_score
        return logs

    @staticmethod
    def _plot_func(scale):
        if scale == "linear":
            plot_func = plt.plot
        elif scale == "semilogx":
            plot_func = plt.semilogx
        elif scale == "semilogy":
            plot_func = plt.semilogy
        elif scale == "loglog":
            plot_func = plt.loglog
        else:
            raise Exception('Only supports scale={"linear", "semilogx", "semilogy", "loglog"}')
        return plot_func


class Checkpoint:
    def __init__(self, model, config, init_epoch=1):
        self.train_cost = []
        self.test_cost = []
        self.train_score = []
        self.test_score = []
        self.best_cost = np.inf
        self.best_score = 0
        self.weights = model.state_dict()
        self.epoch = init_epoch
        self.early_stop = 0
        self.config = config
