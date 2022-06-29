program status
!
!  This code simple takes in a sequence of pointers/paths to:
!  compiled.csv compiled_status.csv compiled_status_pos.csv
!  compiled_status_GEDI_pos.csv
!  


implicit none

character(len=300) :: infile,outfile,out_posfile,out_gedifile

integer :: i, ierr, lines!, dummy

double precision,allocatable :: min_lon(:),min_lat(:), max_lon(:), max_lat(:)
double precision,allocatable :: vg_loss(:), bare_init(:), vh(:), nirg(:), swir(:)
double precision,allocatable :: nasa_elev(:), gedi_elev(:), gedi_loss(:),qual_flag(:)
double precision,allocatable :: b5(:), b6(:), ndmi(:), clon(:),clat(:)
double precision,allocatable :: elev_sc(:), band_sc(:) 
integer,allocatable :: stat(:), stat_with_gedi(:)
character(len=1) :: dummy,sep
character(len=30) :: a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13
character(len=30) :: a14,a15,a16,a17,a18,a19,a20,a21,a22

CALL getarg(1,infile)
CALL getarg(2,outfile)
CALL getarg(3,out_posfile)
CALL getarg(4,out_gedifile)

open(1,file=infile,status='old',action='read')
open(2,file=outfile,status='unknown',action='write')
open(3,file=out_posfile,status='unknown',action='write')
open(4,file=out_gedifile,status='unknown',action='write')

300 format(A1)
100 format(9(f13.8,A1),4(f12.5,A1),5(f13.8,A1),3(i1,A1),i1)
200 format(21(A30,A1),A30)

a1 = 'Minimum Longitude'
a2 = 'Minimum Latitude'
a3 = 'Maximum Longitude'
a4 = 'Maximum Latitude'
a5 = 'Percent Vegetation Loss'
a6 =  'Percent Bare Initial'
a7 = 'Percent Significant VH Values'
a8 = 'Average NIR/G'
a9 =  'Average SWIR1/B'
a10 =  'NASADEM Elevation'
a11 = 'GEDI Elevation'
a12 = 'GEDI-SRTM Elevation'
a13 = 'GEDI Quality Flag'
a14 = 'B5'
a15 =  'B6'
a16 =  'NDMI'
a17 = 'Center Lon'
a18 = 'Center Lat'
a19 = 'Elevation Score' 
a20 = 'Band Variation Score'
a21 = 'Status'
a22 = 'Status_GEDI'

! write headers
write(2,200)a1,sep,a2,sep,a3,sep,a4,sep,a5,sep,a6,sep,a7,sep,&
a8,sep,a9,sep,a10,sep,a11,sep,a12,sep,a13,sep,&
a14,sep,a15,sep,a16,sep,a17,sep,a18,sep,a19,sep,a20,sep,a21,&
sep,a22
write(3,200)a1,sep,a2,sep,a3,sep,a4,sep,a5,sep,a6,sep,a7,sep,&
a8,sep,a9,sep,a10,sep,a11,sep,a12,sep,a13,sep,&
a14,sep,a15,sep,a16,sep,a17,sep,a18,sep,a19,sep,a20,sep,a21,&
sep,a22
write(4,200)a1,sep,a2,sep,a3,sep,a4,sep,a5,sep,a6,sep,a7,sep,&
a8,sep,a9,sep,a10,sep,a11,sep,a12,sep,a13,sep,&
a14,sep,a15,sep,a16,sep,a17,sep,a18,sep,a19,sep,a20,sep,a21,&
sep,a22

sep = ','

lines = 0
do i=1,99999999
lines = lines + 1
read(1,300,iostat=ierr) dummy
if(ierr/=0) exit
end do
rewind 1
lines = lines - 2


allocate( min_lon(lines),min_lat(lines), max_lon(lines), max_lat(lines))
allocate(vg_loss(lines), bare_init(lines), vh(lines), nirg(lines), swir(lines))
allocate(nasa_elev(lines), gedi_elev(lines), gedi_loss(lines),qual_flag(lines))
allocate(b5(lines), b6(lines), ndmi(lines), clon(lines),clat(lines))
allocate( elev_sc(lines), band_sc(lines), stat(lines),stat_with_gedi(lines))

do i=1,1
read(1,*)
end do 

do i=1,lines
read(1,*)min_lon(i),min_lat(i),max_lon(i),max_lat(i),vg_loss(i),bare_init(i),&
vh(i),nirg(i),swir(i),nasa_elev(i),gedi_elev(i),gedi_loss(i),qual_flag(i),&
b5(i),b6(i),ndmi(i),clon(i),clat(i),elev_sc(i),band_sc(i)


! Normal Routine
if(( vg_loss(i) .lt. 20.0d0 ) .and. ( bare_init(i) .gt. 20.d0)  ) then 

    if( ( vh(i) .gt. 25.0d0) .and. (nirg(i) .le. 0.3d0)  .and. (swir(i) .lt.0.65d0  ) &
     .and. (elev_sc(i) .ge. 5)  .and. (band_sc(i).ge.4)  )  then
    stat(i) = 1
    else
    stat(i) = 0
    end if

else 

    if((vg_loss(i) .gt. 20.0d0) .and. (vh(i) .gt. 25.0d0) .and.(nirg(i) .le. 0.3d0 )  .and. (swir(i) .lt. 0.65d0)  ) then 
    stat(i) = 1
    else
    stat(i) = 0
    end if

end if

! GEDI Routine
if(stat(i) .eq. 1)  then
    ! Remove Bad GEDI=-999.0 points
    if( ( (abs(gedi_elev(i)) - 999.0d0) .ge. 0.01d0) .or. ( (abs(gedi_elev(i)) - 999.0d0) .le. -0.01d0) )  then
        ! QF>0 and GEDI_Loss <= 0.0d0
        if((qual_flag(i) .gt. 0.0d0) .and. (gedi_loss(i) .le. 0.0d0 )) then
            stat_with_gedi(i) = 1
        else
            stat_with_gedi(i) = 0
        end if
    else
        stat_with_gedi(i) = 0
    end if

else
stat_with_gedi(i) = 0
end if

write(2,100) min_lon(i),sep,min_lat(i),sep,max_lon(i),sep,max_lat(i),sep,vg_loss(i),sep,bare_init(i),sep,&
vh(i),sep,nirg(i),sep,swir(i),sep,nasa_elev(i),sep,gedi_elev(i),sep,gedi_loss(i),sep,qual_flag(i),sep,&
b5(i),sep,b6(i),sep,ndmi(i),sep,clon(i),sep,clat(i),sep,int(elev_sc(i)),sep,int(band_sc(i)),sep,stat(i),sep,stat_with_gedi(i)

if(stat(i) .eq. 1) write(3,100) min_lon(i),sep,min_lat(i),sep,max_lon(i),sep,max_lat(i),sep,vg_loss(i),sep,bare_init(i),sep,&
vh(i),sep,nirg(i),sep,swir(i),sep,nasa_elev(i),sep,gedi_elev(i),sep,gedi_loss(i),sep,qual_flag(i),sep,&
b5(i),sep,b6(i),sep,ndmi(i),sep,clon(i),sep,clat(i),sep,int(elev_sc(i)),sep,int(band_sc(i)),sep,stat(i),sep,stat_with_gedi(i)


if(stat_with_gedi(i) .eq. 1 ) write(4,100) min_lon(i),sep,min_lat(i),sep,max_lon(i),&
sep,max_lat(i),sep,vg_loss(i),sep,bare_init(i),sep,&
vh(i),sep,nirg(i),sep,swir(i),sep,nasa_elev(i),sep,gedi_elev(i),sep,gedi_loss(i),sep,qual_flag(i),sep,&
b5(i),sep,b6(i),sep,ndmi(i),sep,clon(i),sep,clat(i),sep,int(elev_sc(i)),sep,int(band_sc(i)),sep,stat(i),sep,stat_with_gedi(i)


end do




end program 
