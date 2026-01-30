{
    "name": "Task Management",
    "version": "1.0.1",
    "category": "Tools",
    "summary": "A task management module",
    "author": "internal",
    "depends": ["base"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/task_views.xml",
        "views/project_views.xml",
        "views/tag_views.xml",
        "wizard/task_wizard_views.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
