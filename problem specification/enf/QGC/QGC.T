GIVEN :
TYPES : Object Row Column;
INTTYPES: ;

PREDICATES :
Filled (Row, Column, Object)
Solution (Row, Column, Object)
;

FUNCTIONS :
;

FIND : Solution; 

PHASE :

SATISFYING :
! o: Object r: Row c: Column : Filled (r, c, o)=> Solution (r, c, o) ;
! r: Row c: Column o1: Object o2: Object : (Solution (r, c, o1) & Solution (r, c, o2)) => (o1= o2);
! r: Row o: Object c1: Column c2: Column : (Solution (r, c1, o) & Solution (r, c2, o)) => (c1= c2);
! c: Column o: Object r1: Row r2: Row : (Solution (r1, c, o) & Solution (r2, c, o)) => (r1= r2);


! o: Object r: Row : ? c: Column :Solution (r, c, o) ;
! o: Object c: Column : ? r: Row :Solution (r, c, o) ;
! r: Row c: Column : ? o: Object :Solution (r, c, o) ;

PRINT : Solution;

