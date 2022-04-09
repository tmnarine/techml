#
# Simple R program to demonstrate calculating RMSE using two methods
#	Run: R --no-save < rmse.R
#

#
# Function that uses R constructs
#
rmse_r <- function(actual, predicted)
{
	result <- 0
	if ( length(actual) == length(predicted) )
	{
		result <- sqrt(mean((actual - predicted) ^2 ))
	}
	return(result)
}

#
# Function that uses basic programming principles
#
rmse_b <- function(actual, predicted)
{
	result <- 0
	la <- length(actual)
	lp <- length(predicted)
	if ( la == lp )
	{
		# R is index based starting at 1
		i <- 1
		result <- 0
		# list repeat 0 by la times
		l <- rep(0, la)
		for (a in actual)
		{
			diff <- a - predicted[i]
			l[i] <- diff ^ 2
			# l-value is unlike c/c++
			i + 1 -> i
		}
		result <- sqrt(sum(l)/la)
	}
	return(result)
}

# Build the data and run the calculations
main <- function()
{
	print("# rmse")
	
	# Build the actual and predicted values
	n <- 100
	actual <- rnorm(n)
	predicted <- rnorm(n)
	
	# Check rmse by uncommenting the following lines
	# n <- 5
	# actual <- c(10,10,10,10,10)
	# predicted <- c(12,12,12,12,12)
	
	rmser <- rmse_r(actual, predicted)
	print(paste("    rmse_r: ", rmser))
	
	rmseb <- rmse_b(actual, predicted)
	print(paste("    rmse_b: ", rmseb))
	
	if (abs(rmser-rmseb) > 1e-6)
	{
		print("    rmse error")
	}
	else
	{
		print("    success: rmser == rmseb")
	}
}

main()

