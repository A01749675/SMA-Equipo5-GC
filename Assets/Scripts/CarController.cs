using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarController : MonoBehaviour
{
    [SerializeField]
    GameObject carPrefab;
    [SerializeField]
    GameObject carPrefab2;
    [SerializeField]
    GameObject carPrefab3;
    [SerializeField]
    GameObject carPrefab4;
    public bool callForNextPos;
    public bool waitingForNextPos;
    [SerializeField]
    Connection con;
    bool started;
    public int numberOfCars;
    public List<float> startx;
    public List<float> startz;
    public List<string> startangle ;
    
    List<GameObject> cars; // Initialize the list

    List<bool> arrived;

    // Start is called before the first frame update
    void Start()
    {
        started = false;
        waitingForNextPos = false;
        callForNextPos = true;
        startx = new List<float>();
        startz = new List<float>();
        startangle = new List<string>();
        cars = new List<GameObject>();
        arrived = new List<bool>();
        
    }

    // Update is called once per frame
    void Update()
    {
        if(!started){
            //DebugLog("Not started");
            if(!callForNextPos && !con.addingPos){
                for (int i = 0; i < numberOfCars; i++)
                    {
                    GameObject car = new GameObject("EmptyObject");
                    car.AddComponent<Movement>();
                    Movement movement = car.GetComponent<Movement>();
                    if (i % 4 == 0)
                    {
                        movement.carPrefab = carPrefab;
                    }
                    else if (i % 3 == 0)
                    {
                        movement.carPrefab = carPrefab2;
                    }
                    else if (i % 2 == 0)
                    {
                        movement.carPrefab = carPrefab3;
                    }
                    else
                    {
                        movement.carPrefab = carPrefab4;
                    }
                    movement.id = i;
                    car.name = "Car" + i;
                    cars.Add(car); 
                    movement.con = con;
                    movement.setAngle(startangle[i]);
                    movement.setX(startx[i]);
                    movement.setZ(startz[i]);
                    arrived.Add(false);
                    movement.carController = this;
                    //movement.getStarted = true;
                    movement.setInitialPos(startx[i],startz[i],startangle[i]);
                    movement.getStarted=true;
                }
                started = true;
            }
        }
        /*else{
            bool allCarsReady = true;
            foreach (GameObject car in cars)
            {
                Movement movement = car.GetComponent<Movement>();
                //Debug.Log("Car " + movement.id + " " + movement.callForNextPos);
                if (!movement.callForNextPos)
                {
                    allCarsReady = false;
                    break;
                }
            }

            if (allCarsReady && !waitingForNextPos)
            {
                //Debug.Log("Calling for next pos");
                foreach (GameObject car in cars)
                {
                    Movement movement = car.GetComponent<Movement>();
                    movement.waitingForNextPos = true;
                }
                callForNextPos = true;
            } else{
                Debug.Log("Not all cars ready");
            }
            /*else {
                foreach (GameObject car in cars)
            {
                Movement movement = car.GetComponent<Movement>();
                movement.callForNextPos = false;
                movement.waitingForNextPos = false;
                movement.getStarted = true;
            } 

            }
        }*/
    }

    public void setX(float x, int id)
    {
        if(started){
            if(!arrived[id]){
                GameObject car = cars[id];
                Movement movement = car.GetComponent<Movement>();
                movement.setX(x);
            }
        } else {
            startx.Add(x);
        }
    }
    public void setZ(float z, int id)
    {
        if(started){
            if(!arrived[id]){
                GameObject car = cars[id];
                Movement movement = car.GetComponent<Movement>();
                movement.setZ(z);
            }
        } else{
            startz.Add(z);
        }
    }
    public void setAngle(string direction, int id)
    {
        if(started){
            if(!arrived[id]){
                GameObject car = cars[id];
                Movement movement = car.GetComponent<Movement>();
                movement.setAngle(direction);
                movement.callForNextPos = false;
                movement.waitingForNextPos = false;
                movement.getStarted = true;
            }
        }
        else{
            startangle.Add(direction);
        }
    }
    public void setNoC(int noC)
    {
        numberOfCars = noC;
    }
    public void setArrived(int id)
    {
        if(started){
            //Debug.Log("Car "+id+" has arrived");
            GameObject car = cars[id];
            Movement movement = car.GetComponent<Movement>();
            movement.setArrived();
            arrived[id] = true;
        }
    }

    public void trycalling(){
        bool allCarsReady = true;
            foreach (GameObject car in cars)
            {
                Movement movement = car.GetComponent<Movement>();
                //Debug.Log("Car " + movement.id + " " + movement.callForNextPos);
                if (!movement.callForNextPos)
                {
                    allCarsReady = false;
                    break;
                }
            }

            if (allCarsReady && !waitingForNextPos)
            {
                //Debug.Log("Calling for next pos");
                foreach (GameObject car in cars)
                {
                    Movement movement = car.GetComponent<Movement>();
                    movement.waitingForNextPos = true;
                }
                callForNextPos = true;
            } else{
                //Debug.Log("Not all cars ready");
            }
    }
}