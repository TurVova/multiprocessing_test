import os
import queue
import shutil
import unittest

from uploader import Uploader


class UploaderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.num_of_processes = 4
        cls.files_to_upload = []
        cls.path_for_files = os.path.dirname(os.path.abspath(__file__)) + '/files'
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
            self.files_to_upload,
            self.num_of_processes,
            self.q
        )

    def test_uploader(self):
        self.uploader.start()
        try:
            while self.uploader.is_active():
                progress = self.q.get()
                print(progress.done, progress._error, progress._total)
        except KeyboardInterrupt:
            self.uploader.stop()

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

    def test_queue(self):
        self.assertIsNotNone(self.uploader.performance_tasks)
        self.assertIsNotNone(self.uploader.completed_tasks)
        self.assertIsNotNone(self.uploader.tasks_with_errors)

    def test_report(self):
        report = self.uploader.report(self.uploader.performance_tasks)
        self.assertIsInstance(report, str)

    def test_is_active(self):
        is_active = self.uploader.is_active()
        self.assertIn(is_active, (True, None))


if __name__ == '__main__':
    unittest.main()
