# coding=utf-8
# Copyright 2018 The TF-Agents Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for tf_agents.drivers.dynamic_step_driver."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from tf_agents.drivers import dynamic_step_driver
from tf_agents.drivers import test_utils as driver_test_utils
from tf_agents.environments import tf_py_environment
from tf_agents.specs import tensor_spec
from tf_agents.utils import test_utils


class DynamicStepDriverTest(test_utils.TestCase):

  def testOneStepUpdatesObservers(self):
    if tf.executing_eagerly():
      self.skipTest('b/123880556')

    env = tf_py_environment.TFPyEnvironment(
        driver_test_utils.PyEnvironmentMock())
    policy = driver_test_utils.TFPolicyMock(env.time_step_spec(),
                                            env.action_spec())
    policy_state_ph = tensor_spec.to_nest_placeholder(
        policy.policy_state_spec,
        default=0,
        name_scope='policy_state_ph',
        outer_dims=(1,))
    num_episodes_observer = driver_test_utils.NumEpisodesObserver()

    driver = dynamic_step_driver.DynamicStepDriver(
        env, policy, observers=[num_episodes_observer])
    run_driver = driver.run(policy_state=policy_state_ph)

    with self.session() as session:
      session.run(tf.compat.v1.global_variables_initializer())
      _, policy_state = session.run(run_driver)
      for _ in range(4):
        _, policy_state = session.run(
            run_driver, feed_dict={policy_state_ph: policy_state})
      self.assertEqual(self.evaluate(num_episodes_observer.num_episodes), 2)

  def testMultiStepUpdatesObservers(self):
    env = tf_py_environment.TFPyEnvironment(
        driver_test_utils.PyEnvironmentMock())
    policy = driver_test_utils.TFPolicyMock(env.time_step_spec(),
                                            env.action_spec())
    num_episodes_observer = driver_test_utils.NumEpisodesObserver()

    driver = dynamic_step_driver.DynamicStepDriver(
        env, policy, num_steps=5, observers=[num_episodes_observer])

    run_driver = driver.run()

    self.evaluate(tf.compat.v1.global_variables_initializer())
    self.evaluate(run_driver)
    self.assertEqual(self.evaluate(num_episodes_observer.num_episodes), 2)

  def testTwoObservers(self):
    env = tf_py_environment.TFPyEnvironment(
        driver_test_utils.PyEnvironmentMock())
    policy = driver_test_utils.TFPolicyMock(env.time_step_spec(),
                                            env.action_spec())
    policy_state = policy.get_initial_state(1)
    num_episodes_observer0 = driver_test_utils.NumEpisodesObserver(
        variable_scope='observer0')
    num_episodes_observer1 = driver_test_utils.NumEpisodesObserver(
        variable_scope='observer1')

    driver = dynamic_step_driver.DynamicStepDriver(
        env,
        policy,
        num_steps=5,
        observers=[num_episodes_observer0, num_episodes_observer1])
    run_driver = driver.run(policy_state=policy_state)

    self.evaluate(tf.compat.v1.global_variables_initializer())
    self.evaluate(run_driver)
    self.assertEqual(self.evaluate(num_episodes_observer0.num_episodes), 2)
    self.assertEqual(self.evaluate(num_episodes_observer1.num_episodes), 2)

  def testOneStepReplayBufferObservers(self):
    if tf.executing_eagerly():
      self.skipTest('b/123880556')

    env = tf_py_environment.TFPyEnvironment(
        driver_test_utils.PyEnvironmentMock())
    policy = driver_test_utils.TFPolicyMock(env.time_step_spec(),
                                            env.action_spec())
    policy_state_ph = tensor_spec.to_nest_placeholder(
        policy.policy_state_spec,
        default=0,
        name_scope='policy_state_ph',
        outer_dims=(1,))
    replay_buffer = driver_test_utils.make_replay_buffer(policy)

    driver = dynamic_step_driver.DynamicStepDriver(
        env, policy, num_steps=1, observers=[replay_buffer.add_batch])

    run_driver = driver.run(policy_state=policy_state_ph)
    rb_gather_all = replay_buffer.gather_all()

    with self.session() as session:
      session.run(tf.compat.v1.global_variables_initializer())
      _, policy_state = session.run(run_driver)
      for _ in range(5):
        _, policy_state = session.run(
            run_driver, feed_dict={policy_state_ph: policy_state})

      trajectories = self.evaluate(rb_gather_all)

    self.assertAllEqual(trajectories.step_type, [[0, 1, 2, 0, 1, 2, 0, 1]])
    self.assertAllEqual(trajectories.observation, [[0, 1, 3, 0, 1, 3, 0, 1]])
    self.assertAllEqual(trajectories.action, [[1, 2, 1, 1, 2, 1, 1, 2]])
    self.assertAllEqual(trajectories.policy_info, [[2, 4, 2, 2, 4, 2, 2, 4]])
    self.assertAllEqual(trajectories.next_step_type, [[1, 2, 0, 1, 2, 0, 1, 2]])
    self.assertAllEqual(trajectories.reward, [[1., 1., 0., 1., 1., 0., 1., 1.]])
    self.assertAllEqual(trajectories.discount, [[1., 0., 1, 1, 0, 1., 1., 0.]])

  def testMultiStepReplayBufferObservers(self):
    env = tf_py_environment.TFPyEnvironment(
        driver_test_utils.PyEnvironmentMock())
    policy = driver_test_utils.TFPolicyMock(env.time_step_spec(),
                                            env.action_spec())
    policy_state = policy.get_initial_state(1)
    replay_buffer = driver_test_utils.make_replay_buffer(policy)

    driver = dynamic_step_driver.DynamicStepDriver(
        env, policy, num_steps=6, observers=[replay_buffer.add_batch])

    run_driver = driver.run(policy_state=policy_state)
    rb_gather_all = replay_buffer.gather_all()

    self.evaluate(tf.compat.v1.global_variables_initializer())
    self.evaluate(run_driver)
    trajectories = self.evaluate(rb_gather_all)

    self.assertAllEqual(trajectories.step_type, [[0, 1, 2, 0, 1, 2, 0, 1]])
    self.assertAllEqual(trajectories.observation, [[0, 1, 3, 0, 1, 3, 0, 1]])
    self.assertAllEqual(trajectories.action, [[1, 2, 1, 1, 2, 1, 1, 2]])
    self.assertAllEqual(trajectories.policy_info, [[2, 4, 2, 2, 4, 2, 2, 4]])
    self.assertAllEqual(trajectories.next_step_type, [[1, 2, 0, 1, 2, 0, 1, 2]])
    self.assertAllEqual(trajectories.reward, [[1., 1., 0., 1., 1., 0., 1., 1.]])
    self.assertAllEqual(trajectories.discount, [[1., 0., 1, 1, 0, 1., 1., 0.]])


if __name__ == '__main__':
  tf.test.main()
