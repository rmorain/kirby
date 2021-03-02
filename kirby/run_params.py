# AUTOGENERATED! DO NOT EDIT! File to edit: 04_run_parameters.ipynb (unless otherwise specified).

__all__ = ['RunParams']

# Cell
import multiprocessing

# Cell
class RunParams():
    def __init__(self,
                model='gpt2',
                data_dir = 'data/',
                data_files = {'train': ['data/wiki.train.raw'], 'valid': ['data/wiki.valid.raw'], 'test': ['data/wiki.test.raw']},
                max_epochs=1,
                debug=True,
                batch_size=8,
                data_set_percentage=1,
                seq_length=32,
                statement_length=16,
                momentum=.9,
                lr=1e-2,
                repo='wikitext-103-raw-v1',
                num_workers=multiprocessing.cpu_count(),
                kb_statements_file=None,
                run_name='test',
                project_name='kirby'
            ):

        self.model = model
        self.data_dir = data_dir
        self.data_files = data_files
        self.max_epochs = max_epochs
        self.debug = debug
        self.batch_size = batch_size
        self.data_set_percentage = data_set_percentage
        self.seq_length = seq_length
        self.statement_length = statement_length
        self.momentum = momentum
        self.lr = lr
        self.repo = repo
        self.num_workers = num_workers
        self.kb_statements_file = kb_statements_file
        self.run_name = run_name
