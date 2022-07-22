program status
!
!  This code simple takes in a sequence of pointers/paths to:
!  compiled.csv compiled_status.csv compiled_status_pos.csv
!  compiled_status_GEDI_pos.csv
!  


implicit none

character(len=300) :: infile,outfile,out_posfile,out_gedifile

integer :: i, ierr, lines!, dummy

double precision :: min_lon,min_lat, max_lon, max_lat
double precision :: vg_loss, bare_init, vh, nirg, swir
double precision :: nasa_elev, gedi_elev, gedi_loss,qual_flag
double precision :: b5, b6, ndmi, clon,clat
double precision :: elev_sc, band_sc 
integer :: stat, stat_with_gedi
character(len=1) :: dummy,sep
character(len=32) :: a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13
character(len=32) :: a14,a15,a16,a17,a18,a19,a20,a21,a22

CALL getarg(1,infile)
CALL getarg(2,outfile)

open(1,file=infile,status='old',action='read')
open(2,file=outfile,status='unknown',action='write')

300 format(A1)
100 format(9(f13.8,A1),4(f12.5,A1),5(f13.8,A1),2(f3.1,A1),i1)
!200 format(20(A32),A32)
200 format(A17,A1,A16,A1,A17,A1,A16,A1,A23,A1,A20,A1,A29,A1,A13,A1,A15,A1,A9,&
A1,A9,A1,A9,A1,A15,A1,A8,A1,A8,A1,A4,A1,A10,A1,A10,A1,A15,A1,A20,A1,A6)

sep = ','

a1 = 'Mininum Longitude'
a2 = 'Minimum Latitude'
a3 = 'Maximum Longitude'
a4 = 'Maximum Latitude'
a5 = 'Percent Vegetation Loss'
a6 =  'Percent Bare Initial'
a7 = 'Percent Significant VH Values'
a8 = 'Average NIR/G'
a9 =  'Average SWIR1/B'
a10 =  'NASA Elev'
a11 = 'GEDI Elev'
a12 = 'Elev Loss'
a13 = 'GEDI Qual. Flag'
a14 = 'B5 Value'
a15 =  'B6 Value'
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
a14,sep,a15,sep,a16,sep,a17,sep,a18,sep,a19,sep,a20,sep,a21!,&a22

do i=1,1
read(1,*)
end do 

do i=1,99999999
read(1,*,END=99) min_lon,min_lat,max_lon,max_lat,vg_loss,bare_init,&
vh,nirg,swir,nasa_elev,gedi_elev,gedi_loss,qual_flag,&
b5,b6,ndmi,clon,clat,elev_sc,band_sc

if ( (min_lon .ge. 25.5d0) .and. (min_lat .le. -10.68d0) .and. (max_lon .le.25.7d0) &
.and. (max_lat .ge. -10.75d0)  )  then

write(2,100) min_lon,sep,min_lat,sep,max_lon,sep,max_lat,sep,vg_loss,sep,bare_init,sep,&
vh,sep,nirg,sep,swir,sep,nasa_elev,sep,gedi_elev,sep,gedi_loss,sep,qual_flag,sep,&
b5,sep,b6,sep,ndmi,sep,clon,sep,clat,sep,elev_sc,sep,band_sc,sep,int(stat)
else
continue 
end if

end do

99 continue


end program 
