!calculate the Euclidean Distance
!python3 -m numpy.f2py -m EulerDist -c EulerDist.f90
!created at 2019/11/5

subroutine distance(n,vector_1,vector_2,sum)
	implicit none
	integer::i
	real::temp
	integer,intent(in)::n
	real,intent(in),dimension(n)::vector_1,vector_2
	real,intent(out)::sum

	sum=0
	do i=1,n
		temp=(vector_1(i)-vector_2(i))**2
		sum=sum+temp
	end do
end subroutine