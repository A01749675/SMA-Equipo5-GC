using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.ProBuilder;
public class Vehicle : MonoBehaviour
{
    

    int vehicleIndex;

    int windowSize;

    int id;

    ProBuilderMesh pbMesh;
    List<Vector3> vertices;
    Matrix4x4 carTranslate;
    Vector3 position;
    Matrix4x4 roty;
    Matrix4x4 pneg;
    Matrix4x4 ppos;

    GameObject carPrefab;

    List<Vector3> positions;

    
    // Start is called before the first frame update

    public void SetId(int id){
        this.id = id;
    }
    
    public void AddPositions(Vector3 position){
        positions.Add(position);
    }
    public void SetPrefab(GameObject carPrefab){
        this.carPrefab = carPrefab;
    }

    public bool MetStartingConditions(){
        return positions.Count >= windowSize;
    }

    void Start()
    {
        windowSize = 4;
    }
    public List<Vector3> Window(){
        return positions.GetRange(positions.Count-windowSize,windowSize);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
