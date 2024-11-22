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
    
    List<GameObject> cars = new List<GameObject>(); // Initialize the list

    // Start is called before the first frame update
    void Start()
    {
        for (int i = 0; i < 5; i++)
        {
            GameObject car = new GameObject("EmptyObject");
            car.AddComponent<Movement>();
            Movement movement = car.GetComponent<Movement>();
            if (i % 4 == 0)
            {
                movement.carPrefab = carPrefab4;
            }
            else if (i % 3 == 0)
            {
                movement.carPrefab = carPrefab3;
            }
            else if (i % 2 == 0)
            {
                movement.carPrefab = carPrefab2;
            }
            else
            {
                movement.carPrefab = carPrefab;
            }
            movement.id = i;
            car.name = "Car" + i;
            //car.transform.position = new Vector3(0, 0, i);
            cars.Add(car); // Add the instantiated car to the list
        }
    }

    // Update is called once per frame
    void Update()
    {
        foreach (GameObject car in cars)
        {
            Movement movement = car.GetComponent<Movement>();
            movement.x = 10;
            movement.z = 1;
        }   
    }
}