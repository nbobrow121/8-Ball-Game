#include "phylib.h"

//Part 1 Functions

phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ){

	phylib_object *newStillBall = (phylib_object *)calloc(1,sizeof(phylib_object));

	if (newStillBall == NULL){
		return NULL;
	}

	newStillBall->type = PHYLIB_STILL_BALL;
	newStillBall->obj.still_ball.number = number;
	newStillBall->obj.still_ball.pos = *pos;
	return newStillBall;

}


phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ){

	phylib_object *newRollingBall = (phylib_object *)calloc(1,sizeof(phylib_object));

	if(newRollingBall == NULL){
		return NULL;
	}

	newRollingBall->type = PHYLIB_ROLLING_BALL;
	newRollingBall->obj.rolling_ball.number = number;
	newRollingBall->obj.rolling_ball.pos = *pos;
	newRollingBall->obj.rolling_ball.vel = *vel;
	newRollingBall->obj.rolling_ball.acc = *acc;

	return newRollingBall;
}

phylib_object *phylib_new_hole( phylib_coord *pos ){

	phylib_object *newHole = (phylib_object *)calloc(1,sizeof(phylib_object));

	if(newHole == NULL){
		return NULL;
	}

	newHole->type = PHYLIB_HOLE;
	newHole->obj.hole.pos = *pos;

	return newHole;

}

phylib_object *phylib_new_hcushion( double y ){

	phylib_object *newHCushion = (phylib_object *)calloc(1,sizeof(phylib_object));

	if(newHCushion == NULL){
		return NULL;
	}

	newHCushion->type = PHYLIB_HCUSHION;
	newHCushion->obj.hcushion.y = y;

	return newHCushion;
}

phylib_object *phylib_new_vcushion( double x ){

	phylib_object *newVCushion = (phylib_object *)calloc(1,sizeof(phylib_object));

	if(newVCushion == NULL){
		return NULL;
	}

	newVCushion->type = PHYLIB_VCUSHION;
	newVCushion->obj.vcushion.x = x;

	return newVCushion;
}

phylib_table *phylib_new_table( void ){

	phylib_table *newTable = (phylib_table *)calloc(1,sizeof(phylib_table));

	if(newTable == NULL){
		return NULL;
	}

	newTable->time = 0.0;

	newTable->object[0] = phylib_new_hcushion(0.0);
	newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
	newTable->object[2] = phylib_new_vcushion(0.0);
	newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

	phylib_coord hole1 = {0.0,0.0};
	newTable->object[4] = phylib_new_hole(&hole1);

	phylib_coord hole2 = {0.0,1350.0};
	newTable->object[5] = phylib_new_hole(&hole2);

	phylib_coord hole3 = {0.0,2700.0};
	newTable->object[6] = phylib_new_hole(&hole3);

	phylib_coord hole4 = {1350.0,0.0};
	newTable->object[7] = phylib_new_hole(&hole4);

	phylib_coord hole5 = {1350.0,1350.0};
	newTable->object[8] = phylib_new_hole(&hole5);

	phylib_coord hole6 = {1350.0,2700.0};
	newTable->object[9] = phylib_new_hole(&hole6);

	for(int i = 10; i < PHYLIB_MAX_OBJECTS; i++){
		newTable->object[i] = NULL;
	}
	return newTable;
}

//Part 2 Functions

void phylib_copy_object( phylib_object **dest, phylib_object **src ){

	// Check if src or the object it points to is NULL
	if (src == NULL || *src == NULL) {
        	*dest = NULL;
        	return;
    	}

	// Allocate memory for copyObject
    	phylib_object *copyObject = (phylib_object *)malloc(sizeof(phylib_object));
    	if (copyObject == NULL) {
        	return;
    	}

	// Copy the contents of the source object to the newly allocated memory
    	memcpy(copyObject, *src, sizeof(phylib_object));
	// Assign the address of the copied object to dest
    	*dest = copyObject;
}

phylib_table *phylib_copy_table( phylib_table *table ){

	// Allocate memory for the new table
	phylib_table *copyNewTable = (phylib_table *)calloc(PHYLIB_MAX_OBJECTS, sizeof(phylib_table));

	if(copyNewTable == NULL || table == NULL){
		return NULL;
	}

	// Iterate through each object in the source table
	for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){

		if(table->object[i] != NULL){
			// Copy the object to the corresponding index in the new table
			phylib_copy_object(&copyNewTable->object[i], &table->object[i]);
		}

		else{
			copyNewTable->object[i] = NULL;
		}
	}
	// Copy the time from the source table to the new table
	copyNewTable->time = table->time;

	// Return the new table
	return copyNewTable;

}

void phylib_add_object( phylib_table *table, phylib_object *object ){

    	for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        	if (table->object[i] == NULL) {
            		table->object[i] = object;
            		break;
        	}
    	}
}

void phylib_free_table( phylib_table *table ){

	if(table != NULL){
		for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
			if(table->object[i] != NULL){
				free(table->object[i]);
				table->object[i] = NULL;
			}
		}
		free(table);
	}
}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){

	phylib_coord difference = {c1.x-c2.x, c1.y-c2.y};

	return difference;
}

double phylib_length( phylib_coord c ){

	double length = sqrt((c.x*c.x)+(c.y*c.y));

	return length;
}

double phylib_dot_product( phylib_coord a, phylib_coord b ){

	return ((a.x*b.x)+(a.y*b.y));
}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){

	double calcDistance;

	// Check the type of the first object
    	switch (obj1->type) {
        	case 1:
			// Based on the type of the first object, calculate distance
            		switch (obj2->type) {
                		case 0:
                    			calcDistance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos)) - PHYLIB_BALL_DIAMETER;
                    			break;
                		case 1:
                    			calcDistance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos)) - PHYLIB_BALL_DIAMETER;
                    			break;
                		case 2:
                    			calcDistance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos)) - PHYLIB_HOLE_RADIUS;
                    			break;
                		case 3:
                    			calcDistance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
                    			break;
                		case 4:
                    			calcDistance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
                    			break;
                		default:
					// Return -1 for unsupported object types
                    			return -1;
            		}
            		break;
        	default:
            		return -1;
    	}

	// Return the calculated distance
    	return calcDistance;
}

//Part 3 Functions

void phylib_roll( phylib_object *new, phylib_object *old, double time ){

	// Check if either object is not a rolling ball
	if(new->type != PHYLIB_ROLLING_BALL && old->type != PHYLIB_ROLLING_BALL){
		return;
	}

	// Update position based on velocity and acceleration
        new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x * time + 0.5 * old->obj.rolling_ball.acc.x * time * time;
        new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y * time + 0.5 * old->obj.rolling_ball.acc.y * time * time;

	// Update velocity based on acceleration
        new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
        new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;

	// Check for velocity reversal along x-axis
	if((new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0){
		new->obj.rolling_ball.vel.x = 0;
		new->obj.rolling_ball.acc.x = 0;
	}

	// Check for velocity reversal along y-axis
	if((new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0){
		new->obj.rolling_ball.vel.y = 0;
		new->obj.rolling_ball.acc.y = 0;
	}
}

unsigned char phylib_stopped( phylib_object *object ){

	double currentSpeed = phylib_length(object->obj.rolling_ball.vel);

	// Check if the object is a rolling ball and if its speed is below the threshold
	if(object->type == PHYLIB_ROLLING_BALL && currentSpeed < PHYLIB_VEL_EPSILON){

		// If so, update object type to a still ball
		object->type = PHYLIB_STILL_BALL;

		// Copy attributes from rolling ball to still ball
		object->obj.still_ball.number = object->obj.rolling_ball.number;
		object->obj.still_ball.pos.x = object->obj.rolling_ball.pos.x;
		object->obj.still_ball.pos.y = object->obj.rolling_ball.pos.y;

		// Return 1 to indicate the object has stopped
		return 1;
	}

	// Return 0 to indicate the object is still in motion
	return 0;
}

void phylib_bounce( phylib_object **a, phylib_object **b ){

	// Check if object 'a' is a rolling ball
	if ((*a)->type == PHYLIB_ROLLING_BALL) {

		// Check the type of object 'b'
        	if ((*b)->type == PHYLIB_HCUSHION) {

			// If 'b' is a horizontal cushion, reverse the vertical velocity and acceleration of 'a'
            		(*a)->obj.rolling_ball.vel.y = -(*a)->obj.rolling_ball.vel.y;
            		(*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.acc.y;

        	} else if ((*b)->type == PHYLIB_VCUSHION) {

			// If 'b' is a vertical cushion, reverse the horizontal velocity and acceleration of 'a'
            		(*a)->obj.rolling_ball.vel.x = -(*a)->obj.rolling_ball.vel.x;
            		(*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.acc.x;

        	} else if ((*b)->type == PHYLIB_HOLE) {

			// If 'b' is a hole, free 'a' if it's not NULL
            		if (*a != NULL) {
                		free(*a);
                		(*a) = NULL;
            		}

        	} else if ((*b)->type == PHYLIB_STILL_BALL || (*b)->type == PHYLIB_ROLLING_BALL) {

			// If 'b' is a still or rolling ball, update its type to rolling ball
			(*b)->type = PHYLIB_ROLLING_BALL;

			// Calculate the collision parameters
            		phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            		phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
            		phylib_coord n = {r_ab.x/phylib_length(r_ab), r_ab.y/phylib_length(r_ab)};

            		double v_rel_n = phylib_dot_product(v_rel, n);

			// Update velocities of objects 'a' and 'b' based on collision
            		(*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            		(*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

            		(*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            		(*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

			// Calculate speeds of objects 'a' and 'b'
            		double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
            		double speed_b = phylib_length((*b)->obj.rolling_ball.vel);

			// Update accelerations of objects 'a' and 'b' based on speeds
            		if (speed_a > PHYLIB_VEL_EPSILON) {

               			(*a)->obj.rolling_ball.acc.x = (-(*a)->obj.rolling_ball.vel.x / speed_a) * PHYLIB_DRAG;
                		(*a)->obj.rolling_ball.acc.y = (-(*a)->obj.rolling_ball.vel.y / speed_a) * PHYLIB_DRAG;
            		}

            		if (speed_b > PHYLIB_VEL_EPSILON) {

                		(*b)->obj.rolling_ball.acc.x = (-(*b)->obj.rolling_ball.vel.x / speed_b) * PHYLIB_DRAG;
                		(*b)->obj.rolling_ball.acc.y = (-(*b)->obj.rolling_ball.vel.y / speed_b) * PHYLIB_DRAG;
            		}
        	}
    	}
}

unsigned char phylib_rolling( phylib_table *t ){

	// Check if the table pointer is NULL and if so return 0
	if(t == NULL){
		return 0;
	}

	int count = 0;

	// Iterate through the objects in the table starting from index 10
	for(int i = 10; i < PHYLIB_MAX_OBJECTS; i++){

		// Check if the object exists and if it is a rolling ball
		if(t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL){

			count++;
		}
	}

	// Return the total count of rolling balls
	return count;
}

phylib_table *phylib_segment( phylib_table *table ){

	if (!table) {
        	return NULL;
    	}

    	int rollingBall = phylib_rolling(table);

    	if (rollingBall <= 0) {
        	return NULL;
    	}

	if(rollingBall > 0 && table != NULL){
    		phylib_table *copyTable = phylib_copy_table(table);
    		copyTable->time = PHYLIB_SIM_RATE;

    		while (copyTable->time <= PHYLIB_MAX_TIME) {

        		for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {

            			if (copyTable->object[i] != NULL && copyTable->object[i]->type == PHYLIB_ROLLING_BALL) {
                			phylib_roll(copyTable->object[i], table->object[i], copyTable->time);

                			if (phylib_stopped(copyTable->object[i]) == 1) {
                    				copyTable->time += table->time;
                    				return copyTable;
                			}
            			}
        		}

        		for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {

            			if (copyTable->object[j] != NULL && copyTable->object[j]->type == PHYLIB_ROLLING_BALL) {

                			for (int k = 0; k < PHYLIB_MAX_OBJECTS; k++) {

                    				if (j != k && copyTable->object[k] != NULL && phylib_distance(copyTable->object[j], copyTable->object[k]) < 0.0) {
                        				phylib_bounce(&copyTable->object[j], &copyTable->object[k]);

                        				if (copyTable->object[k]) {
                            					phylib_stopped(copyTable->object[k]);
                        				}
                        				copyTable->time += table->time;
                        				return copyTable;
                    				}
                			}
            			}
        		}
        		copyTable->time += PHYLIB_SIM_RATE;
    		}
    		return copyTable;
	}
	return NULL;
}

//A2 Part 1 Function to add

char *phylib_object_string( phylib_object *object ){

	static char string[80];
	if (object==NULL){
		snprintf( string, 80, "NULL;" );
		return string;
	}
	switch (object->type){
		case PHYLIB_STILL_BALL:
			snprintf( string, 80,
				"STILL_BALL (%d,%6.1lf,%6.1lf)",
				object->obj.still_ball.number,
				object->obj.still_ball.pos.x,
				object->obj.still_ball.pos.y );
			break;
		case PHYLIB_ROLLING_BALL:
			snprintf( string, 80,
				"ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
				object->obj.rolling_ball.number,
				object->obj.rolling_ball.pos.x,
				object->obj.rolling_ball.pos.y,
				object->obj.rolling_ball.vel.x,
				object->obj.rolling_ball.vel.y,
				object->obj.rolling_ball.acc.x,
				object->obj.rolling_ball.acc.y );
			break;
		case PHYLIB_HOLE:
			snprintf( string, 80,
				"HOLE (%6.1lf,%6.1lf)",
				object->obj.hole.pos.x,
				object->obj.hole.pos.y );
			break;
		case PHYLIB_HCUSHION:
			snprintf( string, 80,
				"HCUSHION (%6.1lf)",
				object->obj.hcushion.y );
			break;
		case PHYLIB_VCUSHION:
			snprintf( string, 80,
				"VCUSHION (%6.1lf)",
				object->obj.vcushion.x );
			break;
	}
	return string;
}
