import java.util.Random;

public class Main {

    // Тестова функція, для якої відомий точний інтеграл
    public static double testFunction(double x) {
        return x * x; // Тестова функція: x^2
    }

    // Основна функція, інтеграл якої потрібно обчислити
    public static double mainFunction(double x) {
        return Math.exp(x * x); // Основна функція: e^(x^2)
    }

    // Функція для обчислення точного значення інтегралу
    public static double calculateExactIntegral(double a, double b) {
        return (b * b * b / 3) - (a * a * a / 3); // Точний інтеграл тестової функції: x^3/3
    }

    // Функція для генерації випадкової точки на координатній площині
    public static double[] generateRandomPoint() {
        Random rand = new Random();
        double x = rand.nextDouble(); // Генерація випадкового x в інтервалі [0, 1]
        double y = rand.nextDouble(); // Генерація випадкового y в інтервалі [0, 1]
        return new double[]{x, y};
    }

    // Функція для обчислення значення підінтегральної функції в заданій точці
    public static double evaluateFunction(double x, boolean isTestFunction) {
        if (isTestFunction) {
            return testFunction(x);
        } else {
            return mainFunction(x);
        }
    }

    // Функція для обчислення інтегралу методом Монте-Карло
    public static double monteCarloIntegration(int numSamples, double a, double b, boolean isTestFunction) {
        double sum = 0.0;
        for (int i = 0; i < numSamples; i++) {
            double[] point = generateRandomPoint();
            double x = a + point[0] * (b - a); // Масштабування x до інтервалу [a, b]
            double y = point[1]; // Значення y залишається таким самим, оскільки генерується у [0, 1]
            double functionValue = evaluateFunction(x, isTestFunction);
            sum += functionValue;
        }
        double average = sum / numSamples;
        return average * (b - a); // Масштабування згортки на весь інтервал [a, b]
    }

    public static void main(String[] args) {
        double a = 0.0; // Початок інтервалу
        double b = 1.0; // Кінець інтервалу
        int numSamples = 1000000; // Кількість випадкових точок
        double exactIntegral = calculateExactIntegral(a, b);
        double monteCarloResultTestFunction = monteCarloIntegration(numSamples, a, b, true);
        double monteCarloResultMainFunction = monteCarloIntegration(numSamples, a, b, false);

        // Розрахунок похибок
        double absoluteErrorTestFunction = Math.abs(exactIntegral - monteCarloResultTestFunction);
        double relativeErrorTestFunction = absoluteErrorTestFunction / exactIntegral;
        System.out.println("Error for test function:");
        System.out.println("Absolute error: " + absoluteErrorTestFunction);
        System.out.println("Relative error: " + relativeErrorTestFunction);

        // Результати
        System.out.println("\nThe exact value of the integral: " + exactIntegral);
        System.out.println("Monte Carlo method for the test function: " + monteCarloResultTestFunction);
        System.out.println("Monte Carlo method for the main function: " + monteCarloResultMainFunction);
    }
}
