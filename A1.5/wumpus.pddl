(define 
	(domain wumpus_cave)
	(:requirements :typing)
	(:types tile components - objects
          agent wall crate empty pit halfcrate arrow fireworks wumpus boundary halfpit vehicle weapons - components
          crate halfcrate - vehicle
          fireworks arrow - weapons)
	(:predicates
		(at ?what - components ?tile - tile)
		(adjEast ?tile-1 - tile ?tile-2 - tile)
		(adjWest ?tile-1 - tile ?tile-2 - tile)
		(adjSouth ?tile-1 - tile ?tile-2 - tile)
		(adjNorth ?tile-1 - tile ?tile-2 - tile)
		(has ?defence - components)
	)
	(:action walk-north
		:parameters (?who - agent ?halfcrate - halfcrate ?crate - crate ?empty - empty ?from - tile ?to - tile ?boundary - boundary ?fireworks - fireworks ?arrow - arrow ?wumpus - wumpus)
		:precondition
		(and
			(adjNorth ?from ?to)
			(adjSouth ?to ?from)
			(at ?who ?from)
			(not (at ?wumpus ?to))
      (not (at ?crate ?to))
      (not (at ?halfcrate ?to))
			(or
				(at ?empty ?to)
				(at ?boundary ?to)
				(at ?fireworks ?to)
				(at ?arrow ?to)			
			)
			(or
				(not (has ?fireworks))
				(not (has ?arrow))
				(has ?fireworks)
				(has ?arrow)
			)
		)
		:effect
		(and
			(when
				(at ?empty ?to)
				(not (at ?empty ?to))
			)
			(when
				(at ?boundary ?to)
				(not (at ?boundary ?to))
			)
			(when
				(at ?fireworks ?to)
				(and
					(not (at ?fireworks ?to))
					(has ?fireworks)
				)
			)
			(when
				(at ?arrow ?to)
				(and
					(not (at ?arrow ?to))
					(has ?arrow)
				)
			)
			(at ?who ?to)
			(not (at ?who ?from))
			(at ?empty ?from)
		)
	)
	(:action walk-south
		:parameters (?who - agent ?empty - empty ?halfcrate - halfcrate ?crate - crate ?from - tile ?to - tile ?boundary - boundary ?fireworks - fireworks ?arrow - arrow ?wumpus - wumpus)
		:precondition
		(and
			(adjSouth ?from ?to)
			(adjNorth ?to ?from)
			(at ?who ?from)
			(not (at ?wumpus ?to))
      (not (at ?halfcrate ?to))
      (not (at ?crate ?to))
			(or
				(at ?empty ?to)
				(at ?boundary ?to)
				(at ?fireworks ?to)
				(at ?arrow ?to)
			)
			(or
				(not (has ?fireworks))
				(not (has ?arrow))
				(has ?fireworks)
				(has ?arrow)
			)
		)
		:effect
		(and
			(when
				(at ?empty ?to)
				(not (at ?empty ?to))
			)
			(when
				(at ?boundary ?to)
				(not (at ?boundary ?to))
			)
			(when
				(at ?fireworks ?to)
				(and
					(not (at ?fireworks ?to))
					(has ?fireworks)
				)
			)
			(when
				(at ?arrow ?to)
				(and
					(not (at ?arrow ?to))
					(has ?arrow)
				)
			)
			(at ?who ?to)
			(not (at ?who ?from))
			(at ?empty ?from)
		)
	)
	(:action walk-east
		:parameters (?who - agent ?empty - empty ?halfcrate - halfcrate ?crate - crate ?from - tile ?to - tile ?boundary - boundary ?fireworks - fireworks ?arrow - arrow ?wumpus - wumpus)
		:precondition
		(and
			(adjEast ?from ?to)
			(adjWest ?to ?from)
			(at ?who ?from)
			(not (at ?wumpus ?to))
      (not (at ?halfcrate ?to))
      (not (at ?crate ?to))
			(or
				(at ?empty ?to)
				(at ?boundary ?to)
				(at ?fireworks ?to)
				(at ?arrow ?to)
			)
			(or
				(not (has ?fireworks))
				(not (has ?arrow))
				(has ?fireworks)
				(has ?arrow)
			)
		)
		:effect
		(and
			(when
				(at ?empty ?to)
				(not (at ?empty ?to))
			)
			(when
				(at ?boundary ?to)
				(not (at ?boundary ?to))
			)
			(when
				(at ?fireworks ?to)
				(and
					(not (at ?fireworks ?to))
					(has ?fireworks)
				)
			)
			(when
				(at ?arrow ?to)
				(and
					(not (at ?arrow ?to))
					(has ?arrow)
				)
			)
			(at ?who ?to)
			(not (at ?who ?from))
			(at ?empty ?from)
		)
	)
	(:action walk-west
		:parameters (?who - agent ?empty - empty ?halfcrate - halfcrate ?crate - crate ?from - tile ?to - tile ?boundary - boundary ?fireworks - fireworks ?arrow - arrow ?wumpus - wumpus)
		:precondition
		(and
			(adjWest ?from ?to)
			(adjEast ?to ?from)
			(at ?who ?from)
			(not (at ?wumpus ?to))
			(not (at ?halfcrate ?to))
			(not (at ?crate ?to))
			(or
				(at ?empty ?to)
				(at ?boundary ?to)
				(at ?fireworks ?to)
				(at ?arrow ?to)
			)
			(or
				(not (has ?fireworks))
				(not (has ?arrow))
				(has ?fireworks)
				(has ?arrow)
			)
		)
		:effect
		(and
			(when
				(at ?empty ?to)
				(not (at ?empty ?to))
			)
			(when
				(at ?boundary ?to)
				(not (at ?boundary ?to))
			)
			(when
				(at ?fireworks ?to)
				(and
					(not (at ?fireworks ?to))
					(has ?fireworks)
				)
			)
			(when
				(at ?arrow ?to)
				(and
					(not (at ?arrow ?to))
					(has ?arrow)
				)
			)
			(at ?who ?to)
			(not (at ?who ?from))
			(at ?empty ?from)
		)
	)
	(:action push-north
		:parameters (?who - agent ?vehicle - vehicle ?weapons - weapons ?empty - empty ?halfpit - halfpit ?halfcrate - halfcrate ?halfcrate1 - halfcrate ?crate - crate ?pit - pit ?from - tile ?to - tile ?afterTo - tile ?afterafterTo - tile)
		:precondition 
		(and
			(adjNorth ?from ?to)
			(adjSouth ?to ?from)
			(adjNorth ?to ?afterTo)
			(adjSouth ?afterTo ?to)
      		(adjNorth ?afterTo ?afterafterTo)
			(adjSouth ?afterafterTo ?afterTo)
			(at ?who ?from)
			(or
        		(at ?weapons ?to)
        		(not (at ?weapons ?to))
     		)
			(or 
			(and
			(at ?crate ?to)
			(at ?pit ?afterTo)
			)
			(and
			(at ?halfcrate ?to)
			(at ?pit ?afterTo)
			)
			(and
			(at ?vehicle ?to)
			
			(or
				(at ?empty ?afterTo)
				(at ?weapons ?afterTo)
				;;(at ?arrow ?afterTo)
			)          
			)
			(and
			(at ?halfcrate ?to)
			(at ?halfcrate1 ?afterTo)
			(or
				(at ?empty ?afterafterTo)
				(at ?pit ?afterafterTo)
				(at ?weapons ?afterafterTo)
			)
			
			)
			(and
			(at ?halfcrate ?to)
			(at ?halfpit ?afterTo)
			)
      		)		
		)
		:effect 
		(and
		(when
			(and
			(at ?halfcrate ?to)
			(at ?pit ?afterTo)
			)
			(and 
				(not (at ?pit ?afterTo))
				(at ?halfpit ?afterTo)
				(not (at ?halfcrate ?to))
			)
		)
      	(when
			(and
        	(at ?vehicle ?to)
          	(or
            (at ?empty ?afterTo)
            (at ?weapons ?afterTo)
          	)
        	)
			(and 
          		(when
            		(at ?empty ?afterTo)
            		(and
					(not (at ?vehicle ?to))
					(at ?vehicle ?afterTo)
					(not (at ?empty ?afterTo))

            		)
          		)
				(when
					(at ?weapons ?afterTo)
					(and
					(not (at ?vehicle ?to))
					(at ?vehicle ?afterTo)
					(at ?weapons ?afterTo)
					)
				)
					
					
			)
		)
		(when
			(and
			(at ?halfcrate ?to)
			(at ?halfpit ?afterTo)
			)
			(and
			(not (at ?halfcrate ?to))
			(not (at ?halfpit ?afterTo))
			(at ?empty ?afterTo)
			)
		)
		(when
			(and
			(at ?halfcrate ?to)
			(at ?halfcrate1 ?afterTo)
			(or
				(at ?empty ?afterafterTo)
				(at ?pit ?afterafterTo)
				(at ?weapons ?afterafterTo)
			)
			)
			(and
			(when
				(at ?empty ?afterafterTo)
				(and
				(not (at ?empty ?afterafterTo))
				(at ?halfcrate1 ?afterafterTo)
				(not (at ?halfcrate1 ?afterTo))
				)
			)
			(when
				(at ?weapons ?afterafterTo)
				(and
				(at ?weapons ?afterafterTo)
				(at ?halfcrate ?afterafterTo)
				)
			)
			(when
				(at ?pit ?afterafterTo)
				(and
				(at ?halfpit ?afterafterTo)
				(not (at ?pit ?afterafterTo))
				(not (at ?halfcrate1 ?afterTo))
				)
			)
          	(at ?halfcrate ?afterTo)
          	(not (at ?halfcrate ?to))
        	)
        

      	)
		(when
			(and
			(at ?crate ?to)
			(at ?pit ?afterTo)
			)
			(and 
			(not (at ?pit ?afterTo))
			(not (at ?crate ?to))
			(at ?empty ?afterTo)
			)
		)
		(when
			(at ?weapons ?to)
			(and
			(not (at ?weapons ?to))
			(has ?weapons)
			)
		)

		(at ?who ?to)
		(not (at ?who ?from))
		(at ?empty ?from)
		)
  	)    
  
	(:action push-south
		:parameters (?who - agent ?vehicle - vehicle ?weapons - weapons ?empty - empty ?halfpit - halfpit ?halfcrate - halfcrate ?halfcrate1 - halfcrate ?crate - crate ?pit - pit ?from - tile ?to - tile ?afterTo - tile ?afterafterTo - tile)
		:precondition 
		(and
			(adjSouth ?from ?to)
			(adjNorth ?to ?from)
			(adjSouth ?to ?afterTo)
			(adjNorth ?afterTo ?to)
      		(adjSouth ?afterTo ?afterafterTo)
			(adjNorth ?afterafterTo ?afterTo)
			(at ?who ?from)
			(or
        		(at ?weapons ?to)
        		(not (at ?weapons ?to))
     		)
			(or 
			(and
			(at ?crate ?to)
			(at ?pit ?afterTo)
			)
			(and
			(at ?halfcrate ?to)
			(at ?pit ?afterTo)
			)
			(and
			(at ?vehicle ?to)
			
			(or
				(at ?empty ?afterTo)
				(at ?weapons ?afterTo)
				;;(at ?arrow ?afterTo)
			)          
			)
			(and
			(at ?halfcrate ?to)
			(at ?halfcrate1 ?afterTo)
			(or
				(at ?empty ?afterafterTo)
				(at ?pit ?afterafterTo)
				(at ?weapons ?afterafterTo)
			)
			
			)
			(and
			(at ?halfcrate ?to)
			(at ?halfpit ?afterTo)
			)
      		)
		)
		:effect 
		(and
		(when
			(and
			(at ?halfcrate ?to)
			(at ?pit ?afterTo)
			)
			(and 
				(not (at ?pit ?afterTo))
				(at ?halfpit ?afterTo)
				(not (at ?halfcrate ?to))
			)
		)
      	(when
			(and
        	(at ?vehicle ?to)
          	(or
            (at ?empty ?afterTo)
            (at ?weapons ?afterTo)
          	)
        	)
			(and 
          		(when
            		(at ?empty ?afterTo)
            		(and
					(not (at ?vehicle ?to))
					(at ?vehicle ?afterTo)
					(not (at ?empty ?afterTo))

            		)
          		)
				(when
					(at ?weapons ?afterTo)
					(and
					(not (at ?vehicle ?to))
					(at ?vehicle ?afterTo)
					(at ?weapons ?afterTo)
					)
				)
					
					
			)
		)
		(when
			(and
			(at ?halfcrate ?to)
			(at ?halfpit ?afterTo)
			)
			(and
			(not (at ?halfcrate ?to))
			(not (at ?halfpit ?afterTo))
			(at ?empty ?afterTo)
			)
		)
		(when
			(and
			(at ?halfcrate ?to)
			(at ?halfcrate1 ?afterTo)
			(or
				(at ?empty ?afterafterTo)
				(at ?pit ?afterafterTo)
				(at ?weapons ?afterafterTo)
			)
			)
			(and
			(when
				(at ?empty ?afterafterTo)
				(and
				(not (at ?empty ?afterafterTo))
				(at ?halfcrate1 ?afterafterTo)
				(not (at ?halfcrate1 ?afterTo))
				)
			)
			(when
				(at ?weapons ?afterafterTo)
				(and
				(at ?weapons ?afterafterTo)
				(at ?halfcrate ?afterafterTo)
				)
			)
			(when
				(at ?pit ?afterafterTo)
				(and
				(at ?halfpit ?afterafterTo)
				(not (at ?pit ?afterafterTo))
				(not (at ?halfcrate1 ?afterTo))
				)
			)
          	(at ?halfcrate ?afterTo)
          	(not (at ?halfcrate ?to))
        	)
        

      	)
		(when
			(and
			(at ?crate ?to)
			(at ?pit ?afterTo)
			)
			(and 
			(not (at ?pit ?afterTo))
			(not (at ?crate ?to))
			(at ?empty ?afterTo)
			)
		)
		(when
			(at ?weapons ?to)
			(and
			(not (at ?weapons ?to))
			(has ?weapons)
			)
		)

		(at ?who ?to)
		(not (at ?who ?from))
		(at ?empty ?from)
		)
  	)
  
	(:action push-east
		:parameters (?who - agent ?vehicle - vehicle ?weapons - weapons ?empty - empty ?halfpit - halfpit ?halfcrate - halfcrate ?halfcrate1 - halfcrate ?crate - crate ?pit - pit ?from - tile ?to - tile ?afterTo - tile ?afterafterTo - tile)
		:precondition 
		(and
			(adjEast ?from ?to)
			(adjWest ?to ?from)
			(adjEast ?to ?afterTo)
			(adjWest ?afterTo ?to)
      		(adjEast ?afterTo ?afterafterTo)
			(adjWest ?afterafterTo ?afterTo)
			(at ?who ?from)
			(or
				(at ?weapons ?to)
				(not (at ?weapons ?to))
			)
			(or 
			(and
			(at ?crate ?to)
			(at ?pit ?afterTo)
			)
			(and
			(at ?halfcrate ?to)
			(at ?pit ?afterTo)
			)
			(and
			(at ?vehicle ?to)
			(or
				(at ?empty ?afterTo)
				(at ?weapons ?afterTo)
				;;(at ?arrow ?afterTo)
			)          
			)
			(and
			(at ?halfcrate ?to)
			(at ?halfcrate1 ?afterTo)
			(or
				(at ?empty ?afterafterTo)
				(at ?pit ?afterafterTo)
				(at ?weapons ?afterafterTo)
			)
			
			)
			(and
			(at ?halfcrate ?to)
			(at ?halfpit ?afterTo)
			)
			)
		
    )
		:effect 
		(and
		(when
		(and
			(at ?halfcrate ?to)
			(at ?pit ?afterTo)
		)
		(and 
			(not (at ?pit ?afterTo))
			(at ?halfpit ?afterTo)
			(not (at ?halfcrate ?to))
		)
		)
      	(when
		
        (at ?vehicle ?to)
		
          	
        
		(and 
        (when
            (at ?empty ?afterTo)
            (and
              (not (at ?vehicle ?to))
              (at ?vehicle ?afterTo)
              (not (at ?empty ?afterTo))

            )
        )
        (when
            (at ?weapons ?afterTo)
            (and
              (not (at ?vehicle ?to))
              (at ?vehicle ?afterTo)
              (at ?weapons ?afterTo)
            )
        )
					
					
		)
		)
		(when
			(and
			(at ?halfcrate ?to)
			(at ?halfpit ?afterTo)
			)
			(and
			(not (at ?halfcrate ?to))
			(not (at ?halfpit ?afterTo))
			(at ?empty ?afterTo)
			)
		)
		(when
			(and
			(at ?halfcrate ?to)
			(at ?halfcrate1 ?afterTo)
			(or
				(at ?empty ?afterafterTo)
				(at ?pit ?afterafterTo)
				(at ?weapons ?afterafterTo)
			)
			)
			(and
			(when
				(at ?empty ?afterafterTo)
				(and
				(not (at ?empty ?afterafterTo))
				(at ?halfcrate1 ?afterafterTo)
				(not (at ?halfcrate1 ?afterTo))
				)
			)
			(when
				(at ?weapons ?afterafterTo)
				(and
				(at ?weapons ?afterafterTo)
				(at ?halfcrate ?afterafterTo)
				)
			)
			(when
				(at ?pit ?afterafterTo)
				(and
				(at ?halfpit ?afterafterTo)
				(not (at ?pit ?afterafterTo))
				(not (at ?halfcrate1 ?afterTo))
				)
			)
			(at ?halfcrate ?afterTo)
			(not (at ?halfcrate ?to))
			)
			

		)
		(when
			(and
			(at ?crate ?to)
			(at ?pit ?afterTo)
			)
			(and 
				(not (at ?pit ?afterTo))
				(not (at ?crate ?to))
				(at ?empty ?afterTo)
			)
		)
		(when
			(at ?weapons ?to)
			(and
			(not (at ?weapons ?to))
			(has ?weapons)
			)
		)

		(at ?who ?to)
		(not (at ?who ?from))
		(at ?empty ?from)
		)
  )
  
	(:action push-west
		:parameters (?who - agent ?vehicle - vehicle ?weapons - weapons ?empty - empty ?halfpit - halfpit ?halfcrate - halfcrate ?halfcrate1 - halfcrate ?crate - crate ?pit - pit ?from - tile ?to - tile ?afterTo - tile ?afterafterTo - tile)
		:precondition 
		(and
			(adjWest ?from ?to)
			(adjEast ?to ?from)
			(adjWest ?to ?afterTo)
			(adjEast ?afterTo ?to)
      		(adjWest ?afterTo ?afterafterTo)
			(adjEast ?afterafterTo ?afterTo)
			(at ?who ?from)
			(or
        		(at ?weapons ?to)
        		(not (at ?weapons ?to))
     		)
			(or 
			(and
			(at ?crate ?to)
			(at ?pit ?afterTo)
			)
			(and
			(at ?halfcrate ?to)
			(at ?pit ?afterTo)
			)
			(and
			(at ?vehicle ?to)
			
			(or
				(at ?empty ?afterTo)
				(at ?weapons ?afterTo)
				;;(at ?arrow ?afterTo)
			)          
			)
			(and
			(at ?halfcrate ?to)
			(at ?halfcrate1 ?afterTo)
			(or
				(at ?empty ?afterafterTo)
				(at ?pit ?afterafterTo)
				(at ?weapons ?afterafterTo)
			)
			
			)
			(and
			(at ?halfcrate ?to)
			(at ?halfpit ?afterTo)
			)
      		)
		)
		:effect 
		(and
		(when
			(and
			(at ?halfcrate ?to)
			(at ?pit ?afterTo)
			)
			(and 
				(not (at ?pit ?afterTo))
				(at ?halfpit ?afterTo)
				(not (at ?halfcrate ?to))
			)
		)
      	(when
			(and
        	(at ?vehicle ?to)
          	(or
            (at ?empty ?afterTo)
            (at ?weapons ?afterTo)
          	)
        	)
			(and 
          		(when
            		(at ?empty ?afterTo)
            		(and
					(not (at ?vehicle ?to))
					(at ?vehicle ?afterTo)
					(not (at ?empty ?afterTo))

            		)
          		)
				(when
					(at ?weapons ?afterTo)
					(and
					(not (at ?vehicle ?to))
					(at ?vehicle ?afterTo)
					(at ?weapons ?afterTo)
					)
				)
					
					
			)
		)
		(when
			(and
			(at ?halfcrate ?to)
			(at ?halfpit ?afterTo)
			)
			(and
			(not (at ?halfcrate ?to))
			(not (at ?halfpit ?afterTo))
			(at ?empty ?afterTo)
			)
		)
		(when
			(and
			(at ?halfcrate ?to)
			(at ?halfcrate1 ?afterTo)
			(or
				(at ?empty ?afterafterTo)
				(at ?pit ?afterafterTo)
				(at ?weapons ?afterafterTo)
			)
			)
			(and
			(when
				(at ?empty ?afterafterTo)
				(and
				(not (at ?empty ?afterafterTo))
				(at ?halfcrate1 ?afterafterTo)
				(not (at ?halfcrate1 ?afterTo))
				)
			)
			(when
				(at ?weapons ?afterafterTo)
				(and
				(at ?weapons ?afterafterTo)
				(at ?halfcrate ?afterafterTo)
				)
			)
			(when
				(at ?pit ?afterafterTo)
				(and
				(at ?halfpit ?afterafterTo)
				(not (at ?pit ?afterafterTo))
				(not (at ?halfcrate1 ?afterTo))
				)
			)
          	(at ?halfcrate ?afterTo)
          	(not (at ?halfcrate ?to))
        	)
        

      	)
		(when
			(and
			(at ?crate ?to)
			(at ?pit ?afterTo)
			)
			(and 
			(not (at ?pit ?afterTo))
			(not (at ?crate ?to))
			(at ?empty ?afterTo)
			)
		)
		(when
			(at ?weapons ?to)
			(and
			(not (at ?weapons ?to))
			(has ?weapons)
			)
		)

		(at ?who ?to)
		(not (at ?who ?from))
		(at ?empty ?from)
		)
  	)
	(:action scare-north
		:parameters (?who - agent ?wumpus - wumpus ?empty - empty ?arrow - arrow ?fireworks - fireworks ?from - tile ?to - tile ?afterTo - tile)
		:precondition 
		(and
			(adjNorth ?from ?to)
			(adjSouth ?to ?from)
			(adjNorth ?to ?afterTo)
			(adjSouth ?afterTo ?to)
			(at ?who ?from)
			(at ?wumpus ?to)
			(or
				(at ?fireworks ?to)
				(at ?arrow ?to)
				(not (at ?fireworks ?to))
				(not (at ?arrow ?to))
			)
			(or
				(at ?empty ?afterTo)
				(at ?fireworks ?afterTo)
				(at ?arrow ?afterTo)
			)
			(has ?fireworks)
		)
		:effect 
		(and
			(when
				(and 
					(or
						(at ?fireworks ?to)
						(at ?arrow ?to)
					)
					(at ?wumpus ?to)
				)
				(not (at ?empty ?to))
			)
			(when
				(and
					(not (at ?fireworks ?to))
					(not (at ?arrow ?to))
					(at ?wumpus ?to)
				)
				(at ?empty ?to) 
			)
      (when
        (at ?empty ?afterTo)
        (not (at ?empty ?afterTo))
      )
			(at ?who ?from)
			(at ?wumpus ?afterTo)
			(not (at ?wumpus ?to))
      
			
			(not (has ?fireworks))
		)
  )
	(:action scare-south
		:parameters (?who - agent ?wumpus - wumpus ?empty - empty ?arrow - arrow ?fireworks - fireworks ?from - tile ?to - tile ?afterTo - tile)
		:precondition 
		(and
			(adjSouth ?from ?to)
			(adjNorth ?to ?from)
			(adjSouth ?to ?afterTo)
			(adjNorth ?afterTo ?to)
			(at ?who ?from)
			(at ?wumpus ?to)
			(or
				(at ?fireworks ?to)
				(at ?arrow ?to)
				(not (at ?fireworks ?to))
				(not (at ?arrow ?to))
			)
			(or
				(at ?empty ?afterTo)
				(at ?fireworks ?afterTo)
				(at ?arrow ?afterTo)
			)
			(has ?fireworks)
		)
		:effect 
		(and
			(when
				(and 
					(or
						(at ?fireworks ?to)
						(at ?arrow ?to)
					)
					(at ?wumpus ?to)
				)
				(not (at ?empty ?to))
			)
			(when
				(and
					(not (at ?fireworks ?to))
					(not (at ?arrow ?to))
					(at ?wumpus ?to)
				)
				(at ?empty ?to) 
			)
      (when
        (at ?empty ?afterTo)
        (not (at ?empty ?afterTo))
      )
			(at ?who ?from)
			(at ?wumpus ?afterTo)
			(not (at ?wumpus ?to))
			
			(not (has ?fireworks))
		)
  )
	(:action scare-east
		:parameters (?who - agent ?wumpus - wumpus ?empty - empty ?arrow - arrow ?fireworks - fireworks ?from - tile ?to - tile ?afterTo - tile)
		:precondition 
		(and
			(adjEast ?from ?to)
			(adjWest ?to ?from)
			(adjEast ?to ?afterTo)
			(adjWest ?afterTo ?to)
			(at ?who ?from)
			(at ?wumpus ?to)
			(or
				(at ?fireworks ?to)
				(at ?arrow ?to)
				(not (at ?fireworks ?to))
				(not (at ?arrow ?to))
			)
			(or
				(at ?empty ?afterTo)
				(at ?fireworks ?afterTo)
				(at ?arrow ?afterTo)
			)
			(has ?fireworks)
		)
		:effect 
		(and
			(when
				(and 
					(or
						(at ?fireworks ?to)
						(at ?arrow ?to)
					)
					(at ?wumpus ?to)
				)
				(not (at ?empty ?to))
			)
			(when
				(and
					(not (at ?fireworks ?to))
					(not (at ?arrow ?to))
					(at ?wumpus ?to)
				)
				(at ?empty ?to) 
			)
      (when
        (at ?empty ?afterTo)
        (not (at ?empty ?afterTo))
      )
			(at ?who ?from)
			(at ?wumpus ?afterTo)
			(not (at ?wumpus ?to))
			(not (has ?fireworks))
		)
  )
	(:action scare-west
		:parameters (?who - agent ?wumpus - wumpus ?empty - empty ?arrow - arrow ?fireworks - fireworks ?from - tile ?to - tile ?afterTo - tile)
		:precondition 
		(and
			(adjWest ?from ?to)
			(adjEast ?to ?from)
			(adjWest ?to ?afterTo)
			(adjEast ?afterTo ?to)
			(at ?who ?from)
			(at ?wumpus ?to)
			(or
				(at ?fireworks ?to)
				(at ?arrow ?to)
				(not (at ?fireworks ?to))
				(not (at ?arrow ?to))
			)
			(or
				(at ?empty ?afterTo)
				(at ?fireworks ?afterTo)
				(at ?arrow ?afterTo)
			)
			(has ?fireworks)
		)
		:effect 
		(and
			(when
				(and 
					(or
						(at ?fireworks ?to)
						(at ?arrow ?to)
					)
					(at ?wumpus ?to)
				)
				(not (at ?empty ?to))
			)
			(when
				(and
					(not (at ?fireworks ?to))
					(not (at ?arrow ?to))
					(at ?wumpus ?to)
				)
				(at ?empty ?to) 
			)
      (when
        (at ?empty ?afterTo)
        (not (at ?empty ?afterTo))
      )
			(at ?who ?from)
			(at ?wumpus ?afterTo)
			(not (at ?wumpus ?to))
			(not (has ?fireworks))
		)
  )
	(:action shoot-north
		:parameters (?who - agent ?wumpus - wumpus ?empty - empty ?arrow - arrow ?from - tile ?to - tile)
		:precondition 
		(and
			(adjNorth ?from ?to)
			(adjSouth ?to ?from)
			(at ?who ?from)
			(at ?wumpus ?to)
			(has ?arrow)
		)
		:effect 
		(and
			(at ?who ?from)
			(not (at ?wumpus ?to))
			(at ?empty ?to)
			(not (has ?arrow))
		)
  )
	(:action shoot-south
		:parameters (?who - agent ?wumpus - wumpus ?empty - empty ?arrow - arrow ?from - tile ?to - tile)
		:precondition 
		(and
			(adjSouth ?from ?to)
			(adjNorth ?to ?from)
			(at ?who ?from)
			(at ?wumpus ?to)
			(has ?arrow)
		)
		:effect 
		(and
			(at ?who ?from)
			(not (at ?wumpus ?to))
			(at ?empty ?to)
			(not (has ?arrow))
		)
  )
	(:action shoot-east
		:parameters (?who - agent ?wumpus - wumpus ?empty - empty ?arrow - arrow ?from - tile ?to - tile)
		:precondition 
		(and
			(adjEast ?from ?to)
			(adjWest ?to ?from)
			(at ?who ?from)
			(at ?wumpus ?to)
			(has ?arrow)
		)
		:effect 
		(and
			(at ?who ?from)
			(not (at ?wumpus ?to))
			(at ?empty ?to)
			(not (has ?arrow))
		)
  )
	(:action shoot-west
		:parameters (?who - agent ?wumpus - wumpus ?empty - empty ?arrow - arrow ?from - tile ?to - tile)
		:precondition 
		(and
			(adjWest ?from ?to)
			(adjEast ?to ?from)
			(at ?who ?from)
			(at ?wumpus ?to)
			(has ?arrow)
		)
		:effect 
		(and
			(at ?who ?from)
			(not (at ?wumpus ?to))
			(at ?empty ?to)
			(not (has ?arrow))
		)
  )
)
	