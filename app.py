from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store tasks temporarily in memory
tasks = []
next_id = 1


@app.route("/")
def home():
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"])
    pending_tasks = total_tasks - completed_tasks

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks
    )


@app.route("/add", methods=["POST"])
def add_task():
    global next_id

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        return render_template(
            "index.html",
            tasks=tasks,
            total_tasks=len(tasks),
            completed_tasks=sum(1 for task in tasks if task["completed"]),
            pending_tasks=sum(1 for task in tasks if not task["completed"]),
            error="Task title cannot be empty."
        )

    task = {
        "id": next_id,
        "title": title,
        "description": description,
        "completed": False
    }

    tasks.append(task)
    next_id += 1

    return redirect(url_for("home"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break

    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    global tasks

    tasks = [task for task in tasks if task["id"] != task_id]

    return redirect(url_for("home"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)