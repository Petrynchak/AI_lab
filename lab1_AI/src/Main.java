import java.util.Arrays;

public class Main {
    private static final int N = 8; // Фіксоване значення N

    // Вивід шахової дошки на екран
    private static void printSolution(int[][] board) {
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
    }

    // Перевірка, чи можна розмістити ферзя на дошці в даній позиції
    private static boolean isSafe(int[][] board, int row, int col) {
        int i, j;

        // Перевірка рядка зліва
        for (i = 0; i < col; i++)
            if (board[row][i] == 1)
                return false;

        // Перевірка верхньої діагоналі зліва
        for (i = row, j = col; i >= 0 && j >= 0; i--, j--)
            if (board[i][j] == 1)
                return false;

        // Перевірка нижньої діагоналі зліва
        for (i = row, j = col; j >= 0 && i < N; i++, j--)
            if (board[i][j] == 1)
                return false;

        return true;
    }

    // Рекурсивна функція для розстановки ферзів на дошці
    private static boolean solveNQUtil(int[][] board, int col) {
        // Базовий випадок: всі ферзі розставлені
        if (col >= N)
            return true;

        // Рекурсивно розставляємо ферзів для кожного стовпця
        for (int i = 0; i < N; i++) {
            if (isSafe(board, i, col)) {
                board[i][col] = 1;

                // Рекурсивний виклик для наступного стовпця
                if (solveNQUtil(board, col + 1))
                    return true;

                // Якщо розміщення ферзя веде до нерозв'язної ситуації, відміна
                board[i][col] = 0;
            }
        }

        // Якщо ферзі не може бути розставлений у поточному стовпці
        return false;
    }

    // Головна функція для розв'язання задачі про ферзів
    public static void solveNQ() {
        int[][] board = new int[N][N];
        for (int[] row : board)
            Arrays.fill(row, 0);

        if (!solveNQUtil(board, 0)) {
            System.out.println("Розв'язок не існує");
            return;
        }

        printSolution(board);
    }

    public static void main(String[] args) {
        solveNQ();
    }
}
