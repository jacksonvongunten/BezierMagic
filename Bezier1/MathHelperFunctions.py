class MathHelperFunctions:

    @staticmethod
    def linspace(start, end, length):
        start = float(start)
        end = float(end)
        delta = (end - start)/length
        return [delta*t for t in range(length)]
    
    @staticmethod
    def factorial(n):
        if n < 2:
            return 1
        return float(n*MathHelperFunctions.factorial(n-1))
    
    @staticmethod
    def choose(n, k):
        return float(MathHelperFunctions.factorial(n) / (MathHelperFunctions.factorial(k)* MathHelperFunctions.factorial(n-k)))