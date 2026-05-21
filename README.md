# SiteSpy

SiteSpy is a collaborative student-built web application for managing site inspection, monitoring, reporting, and technical operations.

The system is divided into:

- Frontend: user interface, navigation, forms, dashboards, responsive pages, and user experience.
- Backend: data models, APIs, authentication, validation, access control, reporting logic, and deployment support.
- Shared: common documentation, interfaces, schemas, and reusable planning resources.

The project is structured for clear team collaboration, branch-based work, pull requests, and individual contribution tracking.

## Project Structure

```text
SiteSpy/
  README.md
  CONTRIBUTING.md
  docs/
    collaborators/
      README.md
      collaborators-sanitized.md
      frontend-team.md
      backend-team.md
      task-allocation.md
      git-workflow.md
  frontend/
    README.md
    src/
  backend/
    README.md
    src/
  shared/
    README.md
  project-management/
    milestones.md
    issues-template.md
    issues-to-create.md
    submission-checklist.md
    github-collaborator-invite-checklist.md
```

## Team Roles

- Frontend team: landing page, navigation, authentication screens, dashboards, forms, responsive layouts, UI states, and frontend documentation.
- Backend team: data models, APIs, authentication, validation, access control, reporting logic, testing, deployment support, and technical documentation.
- Team leader: repository setup, GitHub administration, integration review, pull request review, and final submission coordination.

## Setup

1. Clone the repository with your own GitHub account.
2. Create a branch for your assigned task.
3. Work only in the folders related to your assignment unless a pull request requires shared changes.
4. Commit your own work using your own Git identity.
5. Open a pull request for review before merging.

## Git Workflow Summary

- Frontend branch format: `frontend/<username>-task`
- Backend branch format: `backend/<username>-task`
- Pull requests are required for all student work.
- The team leader reviews and merges approved pull requests.

## No-Secrets Rule

Never commit passwords, tokens, private keys, credentials, `.env` files, or raw collaborator files containing private login information.
