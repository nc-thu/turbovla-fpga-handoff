"""Run the official TurboVLA LIBERO evaluator with release-checkpoint fallback.

The patch is intentionally local to this process: it accepts the released
``model_state_dict`` when no EMA field is present.  All task/episode logic is
left in the upstream evaluator.
"""
from __future__ import annotations

import sys


def main() -> None:
    import turbovla.evaluation.policy as policy_module

    def checkpoint_state_dict(checkpoint):
        if isinstance(checkpoint, dict):
            if isinstance(checkpoint.get("ema_model_state_dict"), dict):
                return checkpoint["ema_model_state_dict"]
            if isinstance(checkpoint.get("model_state_dict"), dict):
                return checkpoint["model_state_dict"]
        raise KeyError("checkpoint has neither ema_model_state_dict nor model_state_dict")

    policy_module._checkpoint_state_dict = checkpoint_state_dict
    from vla_adapter.rollout import main as rollout_main

    rollout_main()


if __name__ == "__main__":
    main()
