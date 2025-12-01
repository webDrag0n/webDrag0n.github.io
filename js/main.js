document.addEventListener('DOMContentLoaded', () => {
    fetch('data/resume.json')
        .then(response => response.json())
        .then(data => {
            renderProfile(data.profile);
            renderEducation(data.education);
            renderExperience(data.experience);
            renderSkills(data.skills);
            renderProjects(data.projects);
            renderAwards(data.awards);
        })
        .catch(error => console.error('Error loading resume data:', error));
});

function renderProfile(profile) {
    document.getElementById('hero-name').textContent = profile.name;
    document.getElementById('hero-title').textContent = profile.title;
    document.getElementById('hero-desc').textContent = profile.summary;
    document.getElementById('about-desc').textContent = profile.about;
    
    const avatarImg = document.getElementById('about-avatar');
    if (avatarImg) avatarImg.src = profile.avatar;

    const emailLink = document.getElementById('email-link');
    if (emailLink) {
        emailLink.href = `mailto:${profile.email}`;
        emailLink.textContent = "Get In Touch";
    }
}

function renderEducation(education) {
    const container = document.getElementById('education-list');
    if (!container) return;

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

    experience.forEach(job => {
        const item = document.createElement('div');
        item.className = 'timeline-item';
        
        let techHtml = '';
        if (job.technologies) {
            techHtml = `<div class="job-tech">
                ${job.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
            </div>`;
        }

        item.innerHTML = `
            <h3 class="job-title">${job.role} <span class="job-company">@ ${job.company}</span></h3>
            <div class="job-date">${job.date}</div>
            <p class="job-desc">${job.description}</p>
            ${techHtml}
        `;
        container.appendChild(item);
    });
}

function renderSkills(skills) {
    const container = document.getElementById('skills-list');
    if (!container) return;

    skills.forEach(category => {
        category.items.forEach(skill => {
            const li = document.createElement('li');
            li.textContent = skill;
            container.appendChild(li);
        });
    });
}

function renderProjects(projects) {
    const container = document.getElementById('projects-grid');
    if (!container) return;

    projects.forEach(project => {
        const card = document.createElement('div');
        card.className = 'project-card';
        
        let techHtml = '';
        if (project.technologies) {
            techHtml = `<div class="job-tech" style="margin-top: auto; padding-top: 15px;">
                ${project.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
            </div>`;
        }

        card.innerHTML = `
            <div class="project-top">
                <div class="folder-icon">📁</div>
                <div class="project-links">
                    <a href="${project.link}" target="_blank">🔗</a>
                </div>
            </div>
            <h3 class="project-title">${project.name}</h3>
            <p class="project-desc">${project.description}</p>
            ${techHtml}
        `;
        container.appendChild(card);
    });
}

function renderAwards(awards) {
    const container = document.getElementById('awards-list');
    if (!container) return;

    awards.forEach(award => {
        const item = document.createElement('div');
        item.className = 'timeline-item';
        item.innerHTML = `
            <h3 class="job-title">${award.title}</h3>
            <div class="job-date">${award.date}</div>
            <p class="job-desc">${award.description}</p>
        `;
        container.appendChild(item);
    });
}
