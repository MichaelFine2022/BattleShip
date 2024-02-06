import java.util.Scanner;
public class Board{

  private String[][] squares;

  public Board(){
    squares = new String[10][10];
    for (int i = 0; i < squares.length;i++)
    {
      for (int j = 0; j < squares[i].length; j++)
      {
        squares[i][j] = "-";
      }
    }
  }

  public String toString(){
    for (int a = 0; a < squares.length; a++)
    {
      System.out.println("");
      for (int j = 0; j < squares[a].length; j++)
      {
        System.out.print(squares[a][j] + " ");
      }
    }
    return "";
  }

  public boolean addShip(int row, int col, int len, boolean horizontal){

    if (row < 0 || col < 0 || row >= squares.length || col >= squares[0].length)
      return false;

    if(horizontal)
    {
      if(col + len > squares.length)
        return false;

     
      for (int i = col; i < col + len; i++)
      {
        if(!squares[row][i].equals("-"))
        {
          return false;
        }
      }

      for (int i = col; i < col + len; i++)
      {
        squares[row][i] = "b";
      }
    }

    else
    {
      if(row + len > squares.length)
        return false;

      for (int i = row; i < row + len; i++)
      {
        if(!squares[i][col].equals("-"))
        {
          return false;
        }
      }

      for (int i = row; i < row + len; i++)
      {
        squares[i][col] = "b";
      }
    }

    return true;
  }

  public boolean foundShip(int len){

    for (int r = 0; r < squares.length; r++)
    {

      for (int c = 0; c < squares[r].length; c++)
      {
        int count = 0;
        while (c < squares[r].length && squares[r][c].equals("b"))
        {
         count++;
          c++;
        }
        if(count == len)
          return true;
      }
    }


    for (int c = 0; c < squares[0].length; c++)
    {
    for (int r = 0; r < squares.length; r++)
    {
      int count = 0;
      while(r < squares.length && squares [r][c].equals("b"))
      {
         count++;
          r++;
        }
        if(count == len)
          return true;
      }
    }

    return false;

  }

  public int shoot(int row, int col){
    if(row < 0 || col < 0 || row >= squares.length || col >= squares[0].length)
      return -1;


    if(squares[row][col].equals("b"))
    {
      squares[row][col] = "x";
      return 1;
    }


    if(squares[row][col].equals("x") || squares[row][col].equals("m"))
      return 2;


    squares[row][col] = "m";
    return 0;

    
  }

  public boolean gameOver(){
    for (String[] r : squares)
    {
      for (String s : r)
      {
        if(s.equals("b"))
        {
          return false;
        }
      }
    }
    return true;
  }

}


public class Battleship
{
  public static void main(String[] args)
  {
    // Set up board and print welcome
    Board b = new Board();
    Scanner scan = new Scanner(System.in);
    System.out.println("Welcome to Battleship!\n");
    boolean addNew = true;

    while(addNew)
    {
      System.out.println("Type \"a\" to add new ship, \"b\" to see the board, \"p\" to play or \"q\" to quit.");
      String ans = scan.nextLine();
      if(ans.toLowerCase().equals("q"))
        return;
      if(ans.toLowerCase().equals("a"))
      {
        // Get parameters for new ship
        System.out.println("Starting in which row?");
        int r = scan.nextInt();
        System.out.println("Starting in which column?");
        int c = scan.nextInt();
        System.out.println("How long?");
        int l = scan.nextInt();
        scan.nextLine();
        System.out.println("Horizontal (h) or vertical (v)?");
        String d = scan.nextLine();
        boolean h = (d.toLowerCase().equals("h"));

        // Call addShip method and return message based on true/false value
        if(b.addShip(r, c, l, h))
        {
          System.out.println("\nNew ship added!\n");
        }
        else
          System.out.println("\nCan't put a ship there!\n");
      }
      else if(ans.toLowerCase().equals("b"))
        System.out.println("\n" + b + "\n");
      else if(ans.toLowerCase().equals("p"))
      {
        if(b.foundShip(3) && b.foundShip(4))
        {
          addNew = false;
          System.out.println("\nOk, let's play!\n");
        }
        else
          System.out.println("\nYou need ships of length 3 and 4 to play!\n");
      }
    }

    // As long as ships remain, play game
    while(!b.gameOver())
    {
      System.out.println("Press \"s\" to shoot at a square, \"b\" to see the board, \"q\" to quit.");
      String ans = scan.nextLine();
      if(ans.toLowerCase().equals("q"))
        return;
      else if(ans.toLowerCase().equals("s")){
        // Get row and column to shoot
        System.out.println("Input row.");
        int r = scan.nextInt();
        System.out.println("Input column.");
        int c = scan.nextInt();

        // Perform shot and store result
        int result = b.shoot(r,c);

        // Choose message based on result
        if(result == 1)
          System.out.println("\nHit!\n");
        else if(result == 0)
          System.out.println("\nMiss!\n");
        else if(result == 2)
          System.out.println("\nYou already tried that.\n");
        else if(result == -1)
          System.out.println("\nInvalid coordinates.\n");
        scan.nextLine();
      }
      else if(ans.toLowerCase().equals("b"))
        System.out.println("\n" + b + "\n");
    }
    System.out.println("Game over!");
  }
}
