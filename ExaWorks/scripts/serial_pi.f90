program calculatePi

  integer*8, parameter :: nSamples = 1000000000
  integer*8 :: i
  integer*8 :: nCircle, nSquare
  real*8    :: randX, randY, distance, pi
  integer   :: timeValues(8)
  
  call date_and_time(VALUES=timeValues)
  write(*,"(A,I2.2,A,I2.2,A,I2.2)") "Start Time = ", timeValues(5), ":", timeValues(6), ":", timeValues(7)

  ! Initialize the random number seed
  call random_seed()

  nCircle = 0
  nSquare = 0
  pi = 0.0
  do i=1, nSamples
    call random_number(randX)
    call random_number(randY)

    distance = randX * randX + randY * randY

    if (distance <= 1) then
      nCircle = nCircle + 1
    end if
    nSquare = nSquare + 1

  end do

  pi = 4.0 * nCircle / nSquare

  write(*,"(A,F15.13)") "Approximation of pi = ", pi

  call date_and_time(VALUES=timeValues)
  write(*,"(A,I2.2,A,I2.2,A,I2.2)") "End Time = ", timeValues(5), ":", timeValues(6), ":", timeValues(7)

end program calculatePi

