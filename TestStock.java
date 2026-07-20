/**
 * TestStock.java
 * Test program for the Stock class.
 * Object Oriented Programming - Module 2, Activity 2.
 */
public class TestStock {
    public static void main(String[] args) {
        // Create a Stock object for Netflix with its symbol and name
        Stock netflix = new Stock("NFLX", "Netflix Corporation");

        // Set the previous closing price and the new current price
        netflix.setPreviousPrice(337.5);
        netflix.setNewPrice(345.23);

        // Display the stock information
        System.out.println("Stock symbol: " + netflix.getSymbol());
        System.out.println("Stock name: " + netflix.getName());
        System.out.printf("Previous closing price: $%.2f%n", netflix.getPreviousClosingPrice());
        System.out.printf("Current price: $%.2f%n", netflix.getCurrentPrice());

        // Display the price-change percentage
        double change = netflix.getChangePercent();
        System.out.printf("Price-change percentage: %.2f%%%n", change);

        // Indicate whether the stock went up or down
        if (change > 0) {
            System.out.println("The stock price has gone up.");
        } else if (change < 0) {
            System.out.println("The stock price has gone down.");
        } else {
            System.out.println("The stock price has not changed.");
        }
    }
}
