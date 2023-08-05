
import gym

from sacking.environment import load_env
from sacking.policy import GaussianPolicy
from sacking.q_network import QNetwork
from sacking.trainer import train


def test_pendulum():
    """Test solving gym Pendulum task (continuous actions)"""

    env = load_env('gym/Pendulum-v0')
    valid_env = load_env('gym/Pendulum-v0')

    assert isinstance(env.observation_space, gym.spaces.Box)
    assert len(env.observation_space.shape) == 1
    obs_dim = env.observation_space.shape[0]

    assert isinstance(env.action_space, gym.spaces.Box)
    assert len(env.action_space.shape) == 1
    action_dim = env.action_space.shape[0]

    policy = GaussianPolicy(obs_dim, action_dim,
                            hidden_layers=[64, 64])
    q_network = QNetwork(obs_dim, action_dim,
                         hidden_layers=[64, 64],
                         num_nets=2)

    train(
        policy, q_network, env,
        batch_size=128,
        learning_rate=0.001,
        num_steps=100000,
        replay_buffer_size=100000,
        rundir='/tmp/test_pendulum',
        validation_env=valid_env,
    )
