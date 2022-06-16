program reduce
implicit none

integer :: lines, ierr,i
double precision :: min_lon,min_lat, max_lon, max_lat
double precision :: vg_loss, bare_init, vh, nirg, swir
double precision :: nasa_elev, gedi_elev, gedi_loss,qual_flag
double precision :: b5, b6, ndmi, clon,clat
integer :: elev_sc, band_sc
integer :: stat, stat_with_gedi
character(len=1) :: dummy,sep

sep = ','

open(1,file='25.95_-11.0_26.65_-10_compiled_status.csv',status='old',action='read')
open(2,file='26.205_-10.77_26.368_-10.71_compiled_status.csv',status='unknown',action='write')


300 format(9(f13.8,A1),4(f12.5,A1),5(f13.8,A1),3(i1,A1),i1)

do i=1,99999999
read(1,300,END=90) min_lon,sep,min_lat,sep,max_lon,sep,max_lat,sep,vg_loss,sep,bare_init,sep,&
vh,sep,nirg,sep,swir,sep,nasa_elev,sep,gedi_elev,sep,gedi_loss,sep,qual_flag,sep,&
b5,sep,b6,sep,ndmi,sep,clon,sep,clat,sep,elev_sc,sep,band_sc,sep,stat,sep,stat_with_gedi

if( (min_lon .ge. 26.205) .and. (max_lon .le. 26.368) .and. (min_lat .ge. -10.77) &
.and. (max_lat .le. -10.71)  ) then

write(2,300) min_lon,sep,min_lat,sep,max_lon,sep,max_lat,sep,vg_loss,sep,bare_init,sep,&
vh,sep,nirg,sep,swir,sep,nasa_elev,sep,gedi_elev,sep,gedi_loss,sep,qual_flag,sep,&
b5,sep,b6,sep,ndmi,sep,clon,sep,clat,sep,elev_sc,sep,band_sc,sep,stat,sep,stat_with_gedi

else
continue
end if

end do


90 continue


end program
