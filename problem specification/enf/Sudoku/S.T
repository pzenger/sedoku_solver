GIVEN :
TYPES : ;
INTTYPES: INT;

PREDICATES :
Filled (INT, INT, INT)
Solution (INT, INT, INT )
;

FUNCTIONS :
N (): INT
;

FIND : Solution; 

PHASE :

SATISFYING :
//assertion!!
N ()* N ()= MAX[INT];

! o: INT r: INT c: INT : Filled (r, c, o)=> Solution (r, c, o) ;

! o: INT r: INT : ? c: INT : Solution (r, c, o) ;
! o: INT c: INT : ? r: INT : Solution (r, c, o) ;
! r: INT c: INT : ? o: INT : Solution (r, c, o) ;

! r: INT c: INT o1: INT o2: INT : (Solution (r, c, o1) & Solution (r, c, o2)) => (o1= o2);
! r: INT o: INT c1: INT c2: INT : (Solution (r, c1, o) & Solution (r, c2, o)) => (c1= c2);
! c: INT o: INT r1: INT r2: INT : (Solution (r1, c, o) & Solution (r2, c, o)) => (r1= r2);

! r: INT c: INT r1: INT c1: INT r2: INT c2: INT o: INT : ( (r1<= N () & r2<= N () & c1<= N () & c2<= N () & Solution ((r- 1)* N ()+ r1, (c- 1)* N ()+ c1, o) & Solution ((r- 1) * N ()+ r2, (c- 1)* N ()+ c2, o) ) => ( (r1= r2) & (c1= c2) ) );

PRINT : Solution;

