using System.Collections;
using System.Collections.Generic;
using UnityEngine;
[System.Serializable]
public class Cars
{
    public List<Car> cars;

    public static Cars CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<Cars>(jsonString);
    }
}
