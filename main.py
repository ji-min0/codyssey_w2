from quiz_data import get_default_quizzes


class QuizGame:
    def __init__(self):
        self.quizzes = get_default_quizzes()
        self.best_score = 0

    def show_menu(self):
        print("=" * 40)
        print(" " * 13 + "Quiz Game Menu")
        print("=" * 40)
        print(" 1  퀴즈 풀기")
        print(" 2  퀴즈 추가")
        print(" 3  퀴즈 목록")
        print(" 4  점수 확인")
        print(" 5  종료")
        print("=" * 40)

    def get_menu_choice(self):
        while True:
            try:
                raw = input("선택: ").strip()
            except (EOFError, KeyboardInterrupt):
                return 5

            if not raw:
                print("[안내] 입력이 없습니다. 1-5 사이의 숫자를 입력하세요.\n")
                continue

            if not raw.isdigit():
                print("[안내] 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.\n")
                continue

            choice = int(raw)
            if choice < 1 or choice > 5:
                print("[안내] 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.\n")
                continue

            return choice

    def play_quiz(self):
        print("\n[퀴즈 풀기 기능은 준비 중입니다.]\n")

    def add_quiz(self):
        print("\n[퀴즈 추가 기능은 준비 중입니다.]\n")

    def show_quiz_list(self):
        print("\n[퀴즈 목록 기능은 준비 중입니다.]\n")

    def show_score(self):
        print("\n[점수 확인 기능은 준비 중입니다.]\n")

    def run(self):
        while True:
            self.show_menu()
            choice = self.get_menu_choice()

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("\n[ 게임 종료 ]")
                break


def main():
    game = QuizGame()
    try:
        game.run()
    except (EOFError, KeyboardInterrupt):
        print("\n[ 게임 종료 ]")


if __name__ == "__main__":
    main()
