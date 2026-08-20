import unittest

from fetch_hackernews_ai_articles import classify, normalize_published, relevance_score


class RadarQualityTests(unittest.TestCase):
    def topic_keys(self, title: str, summary: str = "", tags: str = "") -> set[str]:
        return {item["key"] for item in classify(title, summary, tags)}

    def test_filters_generic_ai_assisted_malware_story(self):
        keys = self.topic_keys(
            "SilkParasite Espionage Campaign Targets Governments",
            "Researchers observed professional malware with traces of AI-assisted development.",
            "Malware / Threat Intelligence",
        )
        self.assertEqual(keys, set())

    def test_filters_generic_phishing_ai_story(self):
        keys = self.topic_keys(
            "Phishing 3.0: Agent Versus Agent",
            "Attackers use artificial intelligence for social engineering.",
            "Phishing / Artificial Intelligence",
        )
        self.assertEqual(keys, set())

    def test_consumer_copilot_security_is_not_coding_topic(self):
        keys = self.topic_keys(
            "Microsoft Copilot Personal Flaws Could Exfiltrate Data",
            "A crafted link could allow data exfiltration from connected apps.",
            "AI Security / Vulnerability",
        )
        self.assertIn("ai_security", keys)
        self.assertNotIn("ai_coding", keys)

    def test_mlflow_story_hits_workflow_and_security(self):
        topics = classify(
            "Attackers Exploit MLflow SSRF Flaw",
            "MLflow tracking server flaw can expose cloud credentials and secrets.",
            "Vulnerability / Artificial Intelligence",
        )
        keys = {item["key"] for item in topics}
        self.assertIn("data_workflow", keys)
        self.assertIn("ai_security", keys)
        self.assertGreaterEqual(relevance_score(topics), 8)

    def test_ai_safety_story_is_kept_as_engineering(self):
        keys = self.topic_keys(
            "OpenAI Pauses Frontier RL Training",
            "The company increased monitoring and model evaluation for AI safety and alignment.",
            "Machine Learning / AI Safety",
        )
        self.assertIn("ai_engineering", keys)

    def test_date_normalization_removes_source_icon(self):
        self.assertEqual(normalize_published("\ue802 Aug 19, 2026"), "2026-08-19")
        self.assertEqual(normalize_published("Aug 8, 2026"), "2026-08-08")


if __name__ == "__main__":
    unittest.main()
