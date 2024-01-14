from pathlib import Path
import sys
import os


class Main:
    def __init__(self):
        # Initialization of all the variables

        self.username = None
        self.application_name = None
        self.notification_message = None
        self.folder = Path(__file__).parent
        self.exit_message = self.message_wrapper(["Exiting ..."])

    # ---------- Initialization for inheritence ----------

    # ------ Basic Functions for the cli application ------

    def clear_screen(self) -> None:
        """Clears the screen"""
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def check_input(self, message: str) -> str:
        """Checks the input of the user and handles the KeyboardInterrupt and EOFError"""
        try:
            text = input(message)
        except KeyboardInterrupt:
            # would be nice to make it so that it returns to the previous function instead of exiting
            print(f"\n{self.exit_message}")
            sys.exit(0)
        except EOFError:
            print(f"\n{self.exit_message}")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(0)
        return text

    def enumerate_list(self, message_list: list, simple: bool = False) -> list:
        """Enumerates the list and returns a list of strings"""
        max_number = len(message_list)
        max_number = len(str(max_number))
        max_number = max(2, max_number)
        if simple:
            enumerated_list = [
                f"{str(i+1):>{max_number}}: {option}" for i, option in enumerate(message_list)
            ]
        else: 
            enumerated_list = [
                f"Press {str(i+1):>{max_number}} for: {option}"
                for i, option in enumerate(message_list)
            ]
        return enumerated_list

    def remove_extra_space(self, message_list: list) -> list:
        if message_list[-1] == " ":
            message_list.pop()
            return self.remove_extra_space(message_list)
        return message_list

    def present_choice(
        self, message_list: list, title: str = None, columns: int = None, clearing:bool = True, persistent:bool = False
    ) -> str:
        """Presents the choice to the user and returns the choice"""

        # Clear terminal for better representation
        if clearing:
            self.clear_screen()

        # --- Default title ---

        header = f"\n\n {self.application_name} {'- '+ title if title else ''}\n\n"
        print(header)

        # bring the message list to a pretty box format
        message = self.message_wrapper(
            message_list,
            # title=title,
            columns=columns
        )
        print(message)

        self.notify(persistent=persistent)

        choice = self.check_input(">> ")
        return choice

    def message_wrapper(
        self,
        message_list: list,
        # title: str = None,
        columns: int = None,
        present: bool = False,
    ) -> str:
        """Wraps the list of strings in a box for better representation"""

        wrapped_message = []

        # --- Column Number  ---
        if columns is None:
            columns = self.column_number(message_list)
        # columns = min(columns,self.column_number(message_list))

        # Get the max length of the message
        max_length = max([len(message) for message in message_list])

        # Initialize the final message variable
        final_message = ""

        # If the max_rows is not specified, then it will be the number of rows that can fit in the terminal
        message_list = self.remove_extra_space(message_list)
        if len(message_list) % columns != 0:
            extra_list = [" " for _ in range(columns - len(message_list) % columns)]
            # remove the extra spaces from the list
            message_list.extend(extra_list)

        for i in range(len(message_list)):
            # if it is the start of the column box then add the box
            if i % columns == 0:
                final_message += "│"
            # Add the message and the spaces to make it look nice
            final_message += f" {message_list[i]:{max_length}} │"
            # if it is the end of the column box then add the box and a new line
            if i % columns == columns - 1 and i != len(message_list) - 1:
                final_message += "\n"

        # Print the messages inside boxes
        overhead_lines = "─┬─".join(["─" * max_length for _ in range(columns)])
        underhead_lines = "─┴─".join(["─" * max_length for _ in range(columns)])

        overhead = f"┌ {overhead_lines} ┐"
        underhead = f"└ {underhead_lines} ┘"

        # Print the box containing the message
        wrapped_message.append(overhead)
        wrapped_message.append(final_message)
        wrapped_message.append(underhead)
        wrapped_message.append("\n\n")
        # print(f"{overhead}\n{final_message}\n{underhead}\n\n")
        wrapped_message = "\n".join(wrapped_message)
        if present:
            print(wrapped_message)
        else:
            return wrapped_message

    def column_number(self, message_list: list) -> int:
        """Returns the number of columns that can fit in the terminal"""
        # Get the max length of the message list
        max_length = max([len(message) for message in message_list]) + 3
        # Get the width of the terminal as of right now
        terminal_width = os.get_terminal_size().columns
        # Set the max columns, as the terminal // max_lenth of the message, or the length of the message list if it is less than 4
        max_columns = min(terminal_width // (max_length), min(len(message_list), 4))
        return max_columns

    def options_loader(
        self,
        options_functions: list,
        options_names: list,
        menu_title: str = None,
        simple: bool = False,
        persistent:bool = False
    ) -> None:
        """Prints the options in a nice format"""

        # Creates a list of the options to be displayed
        option_choice = self.enumerate_list(options_names, simple=simple)
        option_choice.append("Press -1 for: Exit")

        # Starts running the loop
        while True:
            # Prints the options and gets the user input
            # choice = self.message_wrapper(option_choice, title=menu_title)
            choice = self.present_choice(
                message_list=option_choice, title=menu_title,persistent=persistent)
            if choice == "-1":
                # This is exit
                self.exit()

            elif choice in [str(i) for i in range(1, len(options_functions) + 1)]:
                # Runs the commands that were given
                options_functions[int(choice) - 1]()
            elif choice in ["\n", ""]:
                continue
            else:
                # print("Invalid option")
                self.notification_message = "Invalid option"

    def notify(self,persistent:bool = False) -> None:

        if self.notification_message:
            if type(self.notification_message) == list:
                self.message_wrapper(self.notification_message, present=True,columns=1)
            else:
                self.message_wrapper([self.notification_message], present=True)

            if not persistent:
                self.notification_message = None
            self.notification_message = None

    def exit(self) -> None:
        """Exits the application"""
        print("\nExiting...\n\n")
        sys.exit(0)

    # ---------- Functions for the cli application ---------


if __name__ == "__main__":
    app = Main()

    # Unicode for the box
    # https://symbl.cc/en/2502/
