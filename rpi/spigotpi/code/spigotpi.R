#
# spigotpi.R -- generate Pi using the spigot algorithm
#
# http://stanleyrabinowitz.com/bibliography/spigot.pdf
# - contains Pascal version of the algorithm
#
# Run: R --no-save < spigotpi.R
#

pi_as_str <- function(no_decimal)
{
	pi_str <- "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
	if (no_decimal)
	{
		# Make it easy to diff string
		l <- nchar(pi_str)
		pi_str <- paste( "0", substr(pi_str, 1, 1), substr( pi_str, 3, l), sep="" )
	}
	return(pi_str)
}

main <- function(N, dbgInfo)
{
	if ( N < 1 )
	{
		print(paste("Invalid N:", N))
		return
	}
	
	calcLen <- function()
	{
		return(floor(10 * N / 3) + 1)
	}
	
	LEN = calcLen()
	A <- rep(2, LEN)
	
	if (dbgInfo)
	{
		print(paste("LEN =", LEN))
	}
	
	nines <- 0
	predigit <- 0
	spigotpi_str <- ""
	
	j <- 1
	while ( j <= N )
	{
		q <- 0
		
		i <- LEN
		while ( i >= 1 )
		{
			calcX <- function()
			{
				return(10 * A[i] + q * i)
			}
			
			calcPreviousA <- function()
			{
				# %% is modules
				return(x %% (2 * i - 1))
			}
			
			calcQ <- function()
			{
				# %/% is in division
				return( x %/% (2 * i -1))
			}
						
			x <- calcX()
			A[i] <- calcPreviousA()
			q <- calcQ()
			
			i <- i - 1
		}

		calcA0 <- function()
		{
			return(q %% 10)
		}
		
		calcQ2 <- function()
		{
			return(q %/% 10)
		}
		
		A[1] <- calcA0()
		q <- calcQ2()
		
		if ( q == 9 )
		{
			nines <- nines + 1
		}
		else
		{
			newdigit <- predigit
			if ( q == 10 )
			{
				newdigit <- predigit + 1
			}
			
			spigotpi_str <- paste(spigotpi_str, newdigit, sep="")
			
			newdigit <- 9
			if ( q == 10 )
			{
				newdigit <- 0
			}
			
			k <- 1
			while ( k <= nines )
			{
				spigotpi_str <- paste(spigotpi_str, newdigit, sep="")
				k <- k + 1
			}
			
			predigit <- q
			if ( q == 10 )
			{
				predigit <- 0
			}
			
			if ( q != 10 )
			{
				nines <- 0
			}
			
			if ( dbgInfo )
			{
				print(spigotpi_str)
			}
		}
		
		j <- j + 1
	}
	
	print(spigotpi_str)
	
	# Check the result
	pi_str <- pi_as_str(TRUE)
	if ( grepl(spigotpi_str, pi_str) )
	{
		print("success: spigotpi_str matches")
	}
	else
	{
		print("error: spigotpi_str does not match")
	}
}

main(100, FALSE)
