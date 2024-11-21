using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.ProBuilder;


public class Vehicles : MonoBehaviour
{
    List<Vector3> positions;

    public int numVehicles = 1;

    [SerializeField]
    List<GameObject> cars;

    public List<Vehicle> vehicles;
    


    // Start is called before the first frame update
    void Start()
    {
        vehicles = new List<Vehicle>();
        
        for(int i = 0; i < numVehicles; i++){
            Vehicle vehicle = new Vehicle();
            Debug.Log("Created new vehicle");
            vehicle.SetId(i);
            vehicle.SetPrefab(cars[i%cars.Count]);
            vehicles.Add(vehicle);
        }
        
    }

    // Update is called once per frame
    void Update()
    {
        for(int i = 0; i < vehicles.Count; i++){
            
            List<Vector3> window = vehicles[i].Window();
            Debug.Log("Vehicle " + i + " window");
             
             Debug.Log("The vehicle has "+window.Count+" positions in the window");
             Debug.Log("------------");
            foreach(Vector3 position in window){
                Debug.Log(position);
            }
            Debug.Log("------------");
            // Debug.Log("The vehicle has "+vehicles[i].positions.Count+" positions");
            // foreach(Vector3 position in vehicles[i].positions){
            //     Debug.Log(position);
            // }
        }
    }
}
