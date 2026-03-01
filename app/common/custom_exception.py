import sys

class CustomException(Exception):
    def __init__(self, message:str, error_detail:Exception = None):
        self.error_message = self.get_detailed_error_message(message, error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def get_detailed_error_message(message, error_detail):
        _, _, exc_tb = sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        #error_message = f"{message} : {error_detail} : {file_name} : {line_number}"

        return (
            f"{message} |"
            f"Error detail : {error_detail} |"
            f"Error occurred in script : {file_name} |"
            f"Error occurred in line : {line_number}"
        )

    def __str__(self):
        return self.error_message


