import shutil
import unittest
import os
import queue
from uploader import Uploader


class UploaderTest(unittest.TestCase):
    num_of_processes = 4
    files_to_upload = []
    path_for_files = os.path.dirname(os.path.abspath(__file__)) + '/files'

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(cls.path_for_files):
            os.makedirs(cls.path_for_files)

        for i in range(1, 15):
            file = open(f"{cls.path_for_files}/file_{i}.txt", 'w')
            cls.files_to_upload.append(file.name)
            file.close()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.path_for_files)

    def setUp(self):
        self.q = queue.Queue()
        self.uploader = Uploader(
            files_list=self.files_to_upload,
            num_of_processes=self.num_of_processes,
            queue=self.q
        )

    def test_uploader(self):
        self.uploader.start()
        while self.uploader.is_active():
            progress = self.q.get()
            print(progress.done, progress._error, progress._total)

    def test_check_path(self):
        self.assertIsInstance(self.uploader.PATH, str)

    def test_files_to_upload(self):
        self.assertIsInstance(self.uploader.files_list, list)

    def test_num_of_process(self):
        self.assertIsInstance(self.uploader.num_of_processes, int)
        self.assertGreater(
            self.uploader.num_of_processes, 0, 'Need more processes.'
        )

    def test_progress(self):
        self.assertIsNotNone(self.uploader.progress)
        self.assertGreaterEqual(self.uploader.progress.done, 0)
        self.assertGreaterEqual(self.uploader.progress.error, 0)
        self.assertGreaterEqual(self.uploader.progress.total, 0)
        self.assertIsInstance(self.uploader.progress.done, int)
        self.assertIsInstance(self.uploader.progress.error, int)
        self.assertIsInstance(self.uploader.progress.total, int)

if __name__ == '__main__':
    unittest.main()