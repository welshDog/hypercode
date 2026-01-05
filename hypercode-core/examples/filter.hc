#:domain classical

@function: filter_positive (data: List<Int>) -> List<Int>
  @doc: "Filter positive numbers from a list"
  
  @let: result = []
  @for: x in data
    @when: x > 0
      @push: result, x
  
  @return: result

@function: main ()
  @let: input = [1, -2, 3, -4, 5]
  @let: output = filter_positive(input)
  @print: output  # => [1, 3, 5]
