import json

resume_path = "data/resume.json"
with open(resume_path, 'r', encoding='utf-8') as f:
    resume_data = json.load(f)

blogs_en = [
    {
        "title": "Individuals, Organizations, and Autonomy: Why Complex Systems Form 'Organizations'",
        "description": "Explores how complex systems inevitably form organizational structures when facing limited resources, long-term goals, and task complexity. Organizations are autonomous feedback systems, not command chains.",
        "date": "2026-05-13",
        "url": "./blogs/01-individuals-organizations-autonomy.html"
    },
    {
        "title": "AI's First Principles: Why AI's Ultimate Value is Organizational Replacement",
        "description": "Analyzes how AI's economic value fundamentally comes from replacing human labor and organizational capacity. The evolution of AI is about enabling fewer people to control larger organizational power.",
        "date": "2026-05-15",
        "url": "./blogs/02-ai-organizational-replacement.html"
    },
    {
        "title": "Why Current Agents Cannot Yet Replace Large Organizations",
        "description": "Examines why existing agents, despite their capabilities, cannot replace complex organizations. The core issue is not intelligence but the lack of long-term autonomy and continuous existence.",
        "date": "2026-05-17",
        "url": "./blogs/03-agents-limitations.html"
    },
    {
        "title": "Autonomous Intelligence Must Possess Continuous Driving Force",
        "description": "Argues that true autonomous intelligence requires internal driving forces to sustain itself, not external goal assignment. Discusses how existence pressure creates long-term behavioral patterns.",
        "date": "2026-05-19",
        "url": "./blogs/04-continuous-driving-force.html"
    },
    {
        "title": "Why Embodied Intelligence Core is Not Robots but 'Existence Pressure'",
        "description": "Reveals that embodied AI's true essence lies not in mechanical robotics but in the pressure of continuous existence. This pressure drives learning, adaptation, and organizational formation.",
        "date": "2026-05-21",
        "url": "./blogs/05-embodiment-existence-pressure.html"
    },
    {
        "title": "Why Future AI Will Evolve Into Long-Term Digital Individuals",
        "description": "Synthesizes previous arguments to explain why AI's ultimate form will be persistent digital entities with organizational capacity, long-term goals, and continuous existence.",
        "date": "2026-05-23",
        "url": "./blogs/06-future-ai-digital-individuals.html"
    }
]

blogs_zh = [
    {
        "title": "个体、组织与自治：为什么复杂系统最终会形成'组织'",
        "description": "探讨复杂系统在资源有限、目标长期化、任务复杂化后如何必然地形成组织结构。组织的本质是自治反馈系统，而不是命令链。",
        "date": "2026-05-13",
        "url": "./blogs/01-individuals-organizations-autonomy.html"
    },
    {
        "title": "人工智能的第一性原理：为什么AI的终极价值是组织替代",
        "description": "分析人工智能的经济价值如何从根本上来源于对人类劳动力与组织能力的替代。AI发展的方向始终是让更少的人控制更大的组织能力。",
        "date": "2026-05-15",
        "url": "./blogs/02-ai-organizational-replacement.html"
    },
    {
        "title": "为什么现有智能体还无法替代大型组织",
        "description": "分析为什么现有Agent虽然具备一定能力，但仍无法替代复杂组织。核心原因不在于智力不足，而在于缺乏长期自治能力和持续存在能力。",
        "date": "2026-05-17",
        "url": "./blogs/03-agents-limitations.html"
    },
    {
        "title": "自治智能为什么必须具备持续驱动力",
        "description": "论证真正的自治智能必须拥有能够长期维持自身运行的内部驱动力。自治的本质并不是自由，而是必须维持自身存在。",
        "date": "2026-05-19",
        "url": "./blogs/04-continuous-driving-force.html"
    },
    {
        "title": "为什么具身智能的核心不是机器人而是'存在压力'",
        "description": "揭示具身AI的真正本质不在机械机器人，而在于持续存在的压力。这种压力驱动学习、适应和组织形成。",
        "date": "2026-05-21",
        "url": "./blogs/05-embodiment-existence-pressure.html"
    },
    {
        "title": "为什么未来AI会演化为长期持续存在的数字个体",
        "description": "综合前面的论点，解释为什么AI的终极形式将是具有组织能力、长期目标和持续存在的永久实体。",
        "date": "2026-05-23",
        "url": "./blogs/06-future-ai-digital-individuals.html"
    }
]

resume_data['en']['blogs'] = blogs_en
resume_data['zh']['blogs'] = blogs_zh

with open(resume_path, 'w', encoding='utf-8') as f:
    json.dump(resume_data, f, ensure_ascii=False, indent=4)
