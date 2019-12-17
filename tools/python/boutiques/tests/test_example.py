#!/usr/bin/env python

from unittest import TestCase
from boutiques.bosh import bosh
from boutiques import __file__ as bfile
from boutiques.validator import DescriptorValidationError
import subprocess
import os.path as op
import os
import simplejson as json


class TestExample(TestCase):

    def test_example_complete(self):
        descriptor = op.join(op.split(bfile)[0], 'schema/examples/'
                                                 'example-invocation/'
                                                 'example_descriptor.json')
        command = ("bosh example " + descriptor + " -c")
        process = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE)
        output = json.loads(process.stdout.read())

        self.assertTrue(("a1" in output and "b2" in output) or "a2" in output)
        self.assertIn("b1", output)
        self.assertIn("c1", output)
        self.assertIn("c2", output)
        self.assertIn("d1", output)
        self.assertIn("d2", output)

    def test_example_required_only(self):
        descriptor = op.join(op.split(bfile)[0], 'schema/examples/'
                                                 'example-invocation/'
                                                 'example_descriptor.json')
        command = ("bosh example " + descriptor)
        process = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE)
        output = json.loads(process.stdout.read())

        self.assertDictEqual({"b1": "b1", "c2": "c2"}, output)

    @pytest.mark.skip(reason="Discontinued localexec._validateDict")
    def test_example_internal_validator_false_flag(self):
        descriptor = op.join(op.split(bfile)[0], 'schema/examples/'
                                                 'example-invocation/'
                                                 'example_descriptor.json')
        invocation = op.join(op.split(bfile)[0], 'schema/examples/'
                                                 'example-invocation/'
                                                 'example_invocation.json')
        command = ("bosh exec simulate -i " + invocation + " " + descriptor)

        process = subprocess.Popen(command, shell=True,
                                   stderr=subprocess.PIPE)
        error = process.stderr.read().decode("utf-8")

        self.assertIn("d2 (False) flag is set to true or otherwise omitted",
                      error)

    def test_example_requires_group_complete_x10(self):
        descriptor = op.join(op.split(bfile)[0],
                             'tests/docopt/valid/test_valid.json')
        from boutiques.localExec import LocalExecutor
        executor = LocalExecutor(descriptor, None,
                                 {"forcePathType": True,
                                  "destroyTempScripts": True,
                                  "changeUser": True,
                                  "skipDataCollect": True,
                                  "requireComplete": True})

        # Can't create descriptors with mutex group but only one valid example
        # Bosh example is inherently random,
        # Couldn't even inject prederemined input to executor.in_dict
        # because _randomFillInDict clears it
        executor.generateRandomParams(100)
        self.assertGreater(len(executor.in_dict), 0)
