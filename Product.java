import java.util.Scanner;

public class Product
{
    public double setPrice(int category)
    {
        double price;
        // Added code: set the unit price according to the product type
        switch (category)
        {
            case 1:
                price = 4.5;
                break;
            case 2:
                price = 3.5;
                break;
            case 3:
                price = 2.5;
                break;
            default:
                price = 0.0;   // any other value is not a valid product type
                break;
        }
        return price;
    }

    public void credit(double totalPrice)
    {
        // Note: the original declaration was "double parcial;", renamed to
        // "parcialPayment" so it matches the assignment below and the file compiles
        double parcialPayment;
        parcialPayment = totalPrice / 3;
        // Added code: print the remaining balance for each month of the
        // three months interest-free credit
        for (int month = 0; month <= 3; month++)
        {
            System.out.printf("Balance payable of Month %d --->%f\n", month, totalPrice - (month * parcialPayment));
        }
    }

    public static void main(String args[])
    {
        int productType;
        int quantity;
        double totalPrice;
        Scanner selection = new Scanner(System.in);
        System.out.println("Which product would you like to order? 1, 2 or 3?");
        productType = selection.nextInt();
        System.out.println("How many products would you like to order?");
        quantity = selection.nextInt();
        // Added code: create the Product object used to calculate the price and the credit
        Product prod = new Product();
        totalPrice = quantity * prod.setPrice(productType);
        System.out.printf("The total price of your order is: %f\n", totalPrice);
        prod.credit(totalPrice);
    }
}
