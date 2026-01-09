# FizzBuzz in HyperCode (conceptual example)
# This is a placeholder showing what the syntax might look like

#:domain classical

@function: fizzbuzz (n: Int) -> Void
    @doc: "Classic FizzBuzz interview question, HyperCode style"
    
    @for: i in range(1, n + 1)
        @if: i % 15 == 0
            @print: "FizzBuzz"
        @elif: i % 3 == 0
            @print: "Fizz"
        @elif: i % 5 == 0
            @print: "Buzz"
        @else:
            @print: i

@function: main ()
    @run: fizzbuzz(100)
