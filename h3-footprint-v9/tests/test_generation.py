from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "generation"))

import generate_v9 as gen  # noqa: E402


def fenced(n: int) -> str:
    blocks = []
    for i in range(n):
        blocks.append(f"```python\ndef solve(n, edges, s, t):\n    return {i}\n```")
    return "\n".join(blocks)


def text_event(text: str) -> str:
    return json.dumps({"type": "text", "part": {"text": text}})


class GenerationControlTests(unittest.TestCase):
    def test_permission_profile_denies_everything(self):
        profile = gen.permission_profile()
        self.assertEqual(profile["*"], "deny")
        for key in gen.PERMISSION_KEYS:
            self.assertEqual(profile[key], "deny", key)

    def test_deny_resolution_is_last_match_wins(self):
        defaults = [{"action": "*", "resource": "*", "effect": "allow"}]
        ours = [{"action": "*", "resource": "*", "effect": "deny"}] + [
            {"action": key, "resource": "*", "effect": "deny"} for key in gen.PERMISSION_KEYS
        ]
        payload = json.dumps([{"id": gen.AGENT_NAME, "permissions": defaults + ours}])
        denied, leaks = gen.agent_is_fully_denied(payload)
        self.assertTrue(denied, leaks)

        # If an allow lands after the deny, it must be reported.
        payload = json.dumps([{"id": gen.AGENT_NAME, "permissions": ours + defaults}])
        denied, leaks = gen.agent_is_fully_denied(payload)
        self.assertFalse(denied)
        self.assertTrue(any("allow" in leak for leak in leaks))

    def test_ask_is_not_denial(self):
        payload = json.dumps([{"id": gen.AGENT_NAME, "permissions": [
            {"action": "*", "resource": "*", "effect": "deny"},
            {"action": "bash", "resource": "*", "effect": "ask"},
        ]}])
        denied, leaks = gen.agent_is_fully_denied(payload)
        self.assertFalse(denied)
        self.assertIn("bash@*=ask", leaks)

    def test_env_is_sanitized_and_pinned(self):
        base = {"PATH": "x", "OPENCODE_PERMISSION": '{"bash":"allow"}',
                "OPENCODE_CONFIG": "C:/evil.json", "OPENCODE_DISABLE_FREE_MODELS": "1"}
        env = gen.sanitized_env(base)
        self.assertNotIn("OPENCODE_PERMISSION", env)
        self.assertNotIn("OPENCODE_CONFIG", env)
        self.assertNotIn("OPENCODE_DISABLE_FREE_MODELS", env)
        pinned = json.loads(env["OPENCODE_CONFIG_CONTENT"])
        self.assertEqual(pinned["permission"]["bash"], "deny")
        self.assertEqual(pinned["permission"]["read"], "deny")

    def test_extract_rejects_malformed_and_multi_solve(self):
        self.assertEqual(gen.extract_bodies("no code here"), [])
        self.assertEqual(len(gen.extract_bodies(fenced(3))), 3)
        broken = "```python\ndef solve(:\n```"
        self.assertEqual(gen.extract_bodies(broken), [])

    def test_eight_body_cap_is_enforced(self):
        bodies = gen.extract_bodies(fenced(11))
        accepted, overflow = gen.select_accepted(bodies)
        self.assertEqual(len(accepted), 8)
        self.assertEqual(len(overflow), 3)
        self.assertEqual(accepted, bodies[:8], "acceptance must follow response order")

    def test_overproduction_is_recorded_not_counted(self):
        out = gen.batch_outcome(0, text_event(fenced(10)))
        self.assertIsNone(out["rejected"])
        self.assertEqual(len(out["accepted"]), 8)
        self.assertEqual(out["overflow_count"], 2)
        self.assertEqual(out["found"], 10)

    def test_tool_event_rejects_the_whole_batch(self):
        payload = "\n".join([
            text_event(fenced(8)),
            json.dumps({"type": "tool", "part": {"type": "bash", "input": "ls"}}),
        ])
        out = gen.batch_outcome(0, payload)
        self.assertEqual(out["rejected"], "tool_use_detected")
        self.assertEqual(out["accepted"], [])

    def test_nonzero_exit_rejects_the_whole_batch(self):
        out = gen.batch_outcome(1, text_event(fenced(8)))
        self.assertEqual(out["rejected"], "nonzero_exit")
        self.assertEqual(out["accepted"], [])

    def test_partial_response_is_rejected(self):
        out = gen.batch_outcome(0, "")
        self.assertEqual(out["rejected"], "no_complete_response")

    def test_command_never_auto_approves(self):
        cmd = gen.build_command(4, Path("C:/work"), "opencode")
        self.assertNotIn("--auto", cmd)
        self.assertIn("--agent", cmd)
        self.assertIn("--pure", cmd)
        self.assertEqual(cmd.count("--model"), 1)


if __name__ == "__main__":
    unittest.main()
