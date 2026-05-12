let currentLang = 'en';
let resumeData = {};

document.addEventListener('DOMContentLoaded', () => {
    fetch('data/resume.json')
        .then(response => response.json())
        .then(data => {
            resumeData = data;
            renderAll(currentLang);
        })
        .catch(error => console.error('Error loading resume data:', error));

    document.getElementById('lang-toggle').addEventListener('click', () => {
        currentLang = currentLang === 'en' ? 'zh' : 'en';
        renderAll(currentLang);
    });
});

function renderAll(lang) {
    const data = resumeData[lang];
    if (!data) return;

    renderProfile(data.profile, lang);
    renderEducation(data.education);
    renderExperience(data.experience);
    renderResearchExperience(data.research_experience);
    renderBlogs(data.blogs);
    renderPublications(data.publications);
    renderSkills(data.skills);
    renderAwards(data.awards);
    updateStaticText(lang);
}

function updateStaticText(lang) {
    const texts = {
        en: {
            aboutTitle: "About Me",
            skillsIntro: "Here are a few technologies I've been working with recently:",
            experienceTitle: "Where I've Worked",
            researchTitle: "Research Experience",
            blogsTitle: "Blogs & Articles",
            publicationsTitle: "Publications",
            educationTitle: "Education",
            awardsTitle: "Awards",
            contactTitle: "What's Next?",
            contactHeading: "Get In Touch",
            contactDesc: "I'm currently looking for new opportunities, my inbox is always open. Whether you have a question or just want to say hi, I'll try my best to get back to you!",
            contactBtn: "Say Hello",
            heroGreeting: "Hi, my name is"
        },
        zh: {
            aboutTitle: "关于我",
            skillsIntro: "最近我正在使用的技术：",
            experienceTitle: "工作经历",
            researchTitle: "科研经验",
            blogsTitle: "博客与文章",
            publicationsTitle: "发表论文",
            educationTitle: "教育经历",
            awardsTitle: "奖项",
            contactTitle: "下一步？",
            contactHeading: "保持联系",
            contactDesc: "我目前正在寻找新的机会，欢迎随时联系。无论您有问题还是只是想打个招呼，我都会尽力回复！",
            contactBtn: "打个招呼",
            heroGreeting: "你好，我是"
        }
    };

    const t = texts[lang];
    document.getElementById('about-title').textContent = t.aboutTitle;
    document.getElementById('skills-intro').textContent = t.skillsIntro;
    document.getElementById('experience-title').textContent = t.experienceTitle;
    document.getElementById('research-title').textContent = t.researchTitle;
    document.getElementById('blogs-title').textContent = t.blogsTitle;
    document.getElementById('publications-title').textContent = t.publicationsTitle;
    document.getElementById('education-title').textContent = t.educationTitle;
    document.getElementById('awards-title').textContent = t.awardsTitle;
    document.getElementById('contact-title').textContent = t.contactTitle;
    document.getElementById('contact-heading').textContent = t.contactHeading;
    document.getElementById('contact-desc').textContent = t.contactDesc;
    document.getElementById('contact-btn').textContent = t.contactBtn;
    document.getElementById('hero-greeting').textContent = t.heroGreeting;
}

function renderProfile(profile, lang) {
    document.getElementById('hero-name').textContent = profile.name;
    document.getElementById('hero-title').textContent = profile.title;
    document.getElementById('hero-desc').textContent = profile.summary;
    document.getElementById('about-desc').textContent = profile.about;
    
    const avatarImg = document.getElementById('about-avatar');
    if (avatarImg) avatarImg.src = profile.avatar;

    const emailLink = document.getElementById('email-link');
    if (emailLink) {
        emailLink.href = `mailto:${profile.email}`;
        emailLink.textContent = lang === 'en' ? "Get In Touch" : "联系我";
    }
    
    const contactBtn = document.getElementById('contact-btn');
    if (contactBtn) {
        contactBtn.href = `mailto:${profile.email}`;
    }
}

function renderEducation(education) {
    const container = document.getElementById('education-list');
    if (!container) return;
    container.innerHTML = '';

    education.forEach(edu => {
        const item = document.createElement('div');
        item.className = 'timeline-item';
        item.innerHTML = `
            <h3 class="job-title">${edu.school}</h3>
            <div class="job-company">${edu.degree}</div>
            <div class="job-date">${edu.date}</div>
            <p class="job-desc">${edu.description}</p>
        `;
        container.appendChild(item);
    });
}

function renderExperience(experience) {
    const container = document.getElementById('experience-list');
    if (!container) return;
    container.innerHTML = '';

    experience.forEach(job => {
        const item = document.createElement('div');
        item.className = 'timeline-item';
        
        item.innerHTML = `
            <h3 class="job-title">${job.role} <span class="job-company">@ ${job.company}</span></h3>
            <div class="job-date">${job.date}</div>
            <p class="job-desc">${job.description}</p>
        `;
        container.appendChild(item);
    });
}

function renderResearchExperience(research) {
    const container = document.getElementById('research-list');
    if (!container) return;
    container.innerHTML = '';

    research.forEach(item => {
        const div = document.createElement('div');
        div.className = 'timeline-item';
        div.innerHTML = `
            <h3 class="job-title">${item.project}</h3>
            <p class="job-desc">${item.description}</p>
        `;
        container.appendChild(div);
    });
}

function renderBlogs(blogs) {
    const container = document.getElementById('blogs-list');
    if (!container || !blogs) return;
    container.innerHTML = '';

    blogs.forEach(blog => {
        const item = document.createElement('div');
        item.className = 'timeline-item';
        
        item.innerHTML = `
            <h3 class="job-title"><a href="${blog.url}" target="_blank" style="color: var(--text-color); text-decoration: none;">${blog.title}</a></h3>
            <div class="job-date">${blog.date}</div>
            <p class="job-desc">${blog.description}</p>
            <a href="${blog.url}" class="btn" style="padding: 5px 10px; font-size: 0.8rem; margin-top: 10px;">Read More</a>
        `;
        container.appendChild(item);
    });
}

function renderPublications(publications) {
    const container = document.getElementById('publications-list');
    if (!container) return;
    container.innerHTML = '';

    publications.forEach(pub => {
        const item = document.createElement('div');
        item.className = 'timeline-item';
        
        let awardHtml = '';
        if (pub.award) {
            awardHtml = `<span class="tech-tag" style="background-color: rgba(255, 215, 0, 0.1); color: #ffd700; border: 1px solid #ffd700;">🏆 ${pub.award}</span>`;
        }

        item.innerHTML = `
            <h3 class="job-title">${pub.title}</h3>
            <div class="job-company">${pub.venue} | ${pub.role}</div>
            <div class="job-desc" style="font-style: italic; margin-bottom: 5px;">${pub.authors}</div>
            <p class="job-desc">${pub.description}</p>
            <div style="margin-top: 10px;">${awardHtml}</div>
        `;
        container.appendChild(item);
    });
}

function renderSkills(skills) {
    const container = document.getElementById('skills-list');
    if (!container) return;
    container.innerHTML = '';

    skills.forEach(category => {
        category.items.forEach(skill => {
            const li = document.createElement('li');
            li.textContent = skill;
            container.appendChild(li);
        });
    });
}

function renderAwards(awards) {
    const container = document.getElementById('awards-list');
    if (!container) return;
    container.innerHTML = '';

    awards.forEach(award => {
        const item = document.createElement('div');
        item.className = 'timeline-item';
        item.innerHTML = `
            <h3 class="job-title">${award.title}</h3>
            <div class="job-date">${award.date}</div>
        `;
        container.appendChild(item);
    });
}
