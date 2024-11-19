using System.Collections;
using System.Collections.Generic;
using UnityEngine;


[System.Serializable]
public class Stoplights
{
    public List<Stoplight> stoplights;

    public static Stoplights CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<Stoplights>(jsonString);
    }

}
