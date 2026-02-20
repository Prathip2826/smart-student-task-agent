from task_manager import add_task, view_tasks

def menu():
    while True:
        print("\n==== Smart Student Task Agent ====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            task = input("Enter task: ")
            add_task(task)
            print("Task added successfully!")

        elif choice == "2":
            tasks = view_tasks()
            if not tasks:
                print("No tasks available.")
            else:
                print("\nYour Tasks:")
                for i, task in enumerate(tasks, start=1):
                    print(f"{i}. {task}")

        elif choice == "3":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()