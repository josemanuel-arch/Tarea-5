/**
 * Stock.java
 * Models a stock, storing its data and computing its price change.
 * Object Oriented Programming - Module 2, Activity 2.
 */
public class Stock {
    // Data fields
    private String symbol;               // the stock's symbol
    private String name;                 // the stock's name
    private double previousClosingPrice; // the stock price for the previous day
    private double currentPrice;         // the stock price for the current time

    /** Constructor that creates a stock with the specified symbol and name. */
    public Stock(String symbol, String name) {
        this.symbol = symbol;
        this.name = name;
    }

    /** Returns the stock's symbol. */
    public String getSymbol() {
        return symbol;
    }

    /** Returns the stock's name. */
    public String getName() {
        return name;
    }

    /** Returns the previous closing price. */
    public double getPreviousClosingPrice() {
        return previousClosingPrice;
    }

    /** Returns the current price. */
    public double getCurrentPrice() {
        return currentPrice;
    }

    /** Sets the value of the data field previousClosingPrice. */
    public void setPreviousPrice(double previousClosingPrice) {
        this.previousClosingPrice = previousClosingPrice;
    }

    /** Sets the value of the data field currentPrice. */
    public void setNewPrice(double currentPrice) {
        this.currentPrice = currentPrice;
    }

    /**
     * Returns the percentage changed from previousClosingPrice to currentPrice.
     * Formula: ((currentPrice - previousClosingPrice) / previousClosingPrice) * 100
     * The value is positive if the price has gone up and negative if it has gone down.
     */
    public double getChangePercent() {
        return ((currentPrice - previousClosingPrice) / previousClosingPrice) * 100;
    }
}
