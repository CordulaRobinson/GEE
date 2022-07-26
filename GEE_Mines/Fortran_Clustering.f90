program cluster
implicit none

character(len=300) :: infile,outfile,out_posfile
character(len=1) :: sep
integer :: i, ierr, lines, min_lim,fail,ind,j,nres,counter

double precision :: dummy,meter,pixel,top,left,right,down
double precision, allocatable :: lon(:),lat(:)
integer, allocatable :: idx(:), temp(:)

CALL getarg(1,infile)
CALL getarg(2,outfile)

100 format(f9.6)
200 format(f12.6,A1,f12.6)


open(1,file=infile,status='old',action='read')
open(2,file=outfile,status='unknown',action='write')

meter = 0.00001d0
sep = ','
pixel = 30.0d0
nres=7

min_lim = nres**2

lines=0
do i=1,999999999
lines=lines+1
read(1,100,iostat=ierr) dummy
if(ierr/=0) exit
end do
lines=lines-1
rewind(1)

allocate(lon(lines),lat(lines),idx(lines),temp(lines))

do i=1,lines
read(1,*) lon(i),lat(i)
temp(i) = 0
idx(i) = 0
end do

do i=1,lines
    
    left = lon(i) - nres * meter * pixel
    right= lon(i) + nres * meter * pixel
    top   = lat(i) + nres * meter * pixel
    down = lat(i) - nres * meter * pixel
    
    counter=0
    fail=0
    j=0
    do while (counter .lt. min_lim )
        j=j+1
        if((lon(j) .lt. right) .and. (lon(j) .gt. left) .and. (lat(j).lt.top) .and. (lat(j) .gt. down)) then
        counter=counter+1
        temp(counter) = j
        else
        continue
        end if
        
        if(j .eq. lines) then
        fail=1
        counter = min_lim
        else
        continue
        end if
    end do

    if(fail .eq. 0 .and. counter .ge. min_lim) then
        ind = temp(1)
        j=0
        do while (ind .gt. 0)
        j=j+1
        ind = int(temp(j))
        idx(ind) = 1
        end do
    else
    continue
    end if


end do


do i =1,lines
if(idx(i) .ne. 0) then
write(2,200) lon(i),sep,lat(i)
else
continue 
end if
end do





end program
