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
        for(int i = 0; i < numVehicles; i++){
            Vehicle vehicle = new Vehicle();
            vehicle.SetId(i);
            vehicle.SetPrefab(cars[i%cars.Count]);
            vehicles.Add(vehicle);
        }
        
    }

    // Update is called once per frame
    void Update()
    {
        for(int i = 0; i < numVehicles; i++){
            List<Vector3> window = vehicles[i].Window();
            foreach(Vector3 position in window){
                Debug.Log(position);
            }
        }
    }
}
