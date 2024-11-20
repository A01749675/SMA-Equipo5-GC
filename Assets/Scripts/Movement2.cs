using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.ProBuilder;
using UnityEngine.UIElements;

public class Movement2 : MonoBehaviour
{
    
    public float x;
    public float z;
    ProBuilderMesh pbMesh;
    List<Vector3> vertices;
    Matrix4x4 carTranslate;
    Vector3 position;
    Matrix4x4 roty;
    Matrix4x4 pneg;
    Matrix4x4 ppos;
    Vector3 pivot;
    [SerializeField]
    float angle;
    
    Matrix4x4 m;
    float objectiveAngle;
    bool flag;
    Matrix4x4 scale;
    [SerializeField]
    GameObject carPrefab;
    GameObject car;
    [SerializeField]
    Connection con;

    public bool callForNextPos;

    
    
    


    // Start is called before the first frame update
    void Start()
    {
        // Instancia el prefab del coche
        if (carPrefab != null)
        {
            car = Instantiate(carPrefab);
            car.name = "CarPrueba";
        }
        else
        {
            Debug.LogError("Car prefab is not assigned!");
            return;
        }
        pbMesh = car.GetComponent<ProBuilderMesh>();
        vertices =new List<Vector3>(pbMesh.positions);
        carTranslate = VecOps.TranslateM(new Vector3 (x, 0, z) );
        position = new Vector3 (x, 0, z);
        roty = VecOps.RotateYM(angle);
        Debug.Log(angle);
        Debug.Log(roty);
        scale= VecOps.ScaleM(new Vector3 (1,1,1));
        m =  scale*carTranslate *roty;
        Debug.Log(m);
        pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
        pbMesh.ToMesh();
        pbMesh.Refresh();
        pivot = new Vector3 (x,0,z);
        ppos = VecOps.TranslateM(pivot);
        pneg = VecOps.TranslateM(-pivot);
        flag = false;
        
    }

    // Update is called once per frame
    void Update()
    {
       if(AproximadamenteIgual(x,position.x,0.1f) & AproximadamenteIgual(z,position.z,0.1f)){
            //Debug.Log("En objetivo");
            flag = false;
            callForNextPos = true;
            //con.CallNextPos();
            

        } else{
            objectiveAngle = (360+Mathf.Atan2(z-position.z, x-position.x) * Mathf.Rad2Deg)%360;
            if(angle==objectiveAngle){
                if(AproximadamenteIgual(position.x,x,0.1f)){
                    if(position.z < z){
                        move_z(0.1f);
                        //Debug.Log("Arriba");
                    } else{
                        move_z(-0.1f);
                        //Debug.Log("Abajo");
                    }
                }
                else{
                    if(position.x < x){
                        move_x(0.1f);
                        //Debug.Log("Derecha");
                    } else{
                        move_x(-0.1f);
                        //Debug.Log("Izquierda");
                    }
                }
            }
            else{
                if(objectiveAngle > angle ){
                    pivot = new Vector3 (0,0,0.5f);
                    rotate_left();
                } else{
                    pivot = new Vector3 (0,0,-0.5f);
                    rotate_right();
                }
            }
          
        }

        ppos = VecOps.TranslateM(pivot);
        pneg = VecOps.TranslateM(-pivot);
        
        m = scale*carTranslate *ppos * roty * pneg;

        pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
        pbMesh.ToMesh();
        Debug.Log(m);
        pbMesh.Refresh();
    }
    void move_x(float speed)
{
    position.x += speed;
    carTranslate *= VecOps.TranslateM(new Vector3(speed, 0, 0));
}

void move_z(float speed)
{
    position.z += speed;
    carTranslate *= VecOps.TranslateM(new Vector3(0, 0, speed));
}

void rotate_left()
{
    angle++;
    roty *= VecOps.RotateYM(1); // Rotación acumulativa
}

void rotate_right()
{
    angle--;
    roty *= VecOps.RotateYM(-1); // Rotación acumulativa
}

bool AproximadamenteIgual(float valor1, float valor2, float tolerancia = 0.0001f)
{
    return Mathf.Abs(valor1 - valor2) < tolerancia;
}
}

