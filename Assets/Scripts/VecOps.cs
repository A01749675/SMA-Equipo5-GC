using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VecOps 
{

    public static float DotProduct(Vector3 a, Vector3 b)
    {
        return a.x * b.x + a.y * b.y + a.z * b.z;
    }

    public static Vector3 CrossProduct(Vector3 a, Vector3 b)
    {
        float x = a.y * b.z - a.z * b.y;
        float y = a.z * b.x - a.x * b.z;
        float z = a.x * b.y - a.y * b.x;
        return new Vector3(x, y, z);
    }

    public static Vector3 Normalize(Vector3 a)
    {
        float mag = Mathf.Sqrt(a.x * a.x + a.y * a.y + a.z * a.z);
        return new Vector3(a.x / mag, a.y / mag, a.z / mag);
    }

    public static float Angle(Vector3 a, Vector3 b)
    {
        // angle = ACos(Dot(au,bu))
        float angle= Mathf.Acos(DotProduct(Normalize(a), Normalize(b)));
        return angle*Mathf.Rad2Deg;
    }

    public static Matrix4x4 TranslateM(Vector3 dt)
    {
        Matrix4x4 m = Matrix4x4.identity;
        m[0, 3] = dt.x;
        m[1, 3] = dt.y;
        m[2, 3] = dt.z;
        return m;
    }

    public static Matrix4x4 ScaleM(Vector3 ds)
    {
        Matrix4x4 m = Matrix4x4.identity;
        m[0, 0] = ds.x;
        m[1, 1] = ds.y;
        m[2, 2] = ds.z;
        return m;
    }

    public static Matrix4x4 RotateXM(float degrees)
    {
        float radians = degrees * Mathf.Deg2Rad;
        Matrix4x4 m = Matrix4x4.identity;
        m[1, 1] = Mathf.Cos(radians);
        m[1, 2] = -Mathf.Sin(radians);
        m[2, 1] = Mathf.Sin(radians);
        m[2, 2] = Mathf.Cos(radians);
        return m;
    }

    public static Matrix4x4 RotateYM(float degrees)
    {
        float radians = degrees * Mathf.Deg2Rad;
        Matrix4x4 m = Matrix4x4.identity;
        m[0, 0] = Mathf.Cos(radians);
        m[0, 2] = Mathf.Sin(radians);
        m[2, 0] = -Mathf.Sin(radians);
        m[2, 2] = Mathf.Cos(radians);
        return m;
    }

    public static Matrix4x4 RotateZM(float degrees)
    {
        float radians = degrees * Mathf.Deg2Rad;
        Matrix4x4 m = Matrix4x4.identity;
        m[0, 0] = Mathf.Cos(radians);
        m[0, 1] = -Mathf.Sin(radians);
        m[1, 0] = Mathf.Sin(radians);
        m[1, 1] = Mathf.Cos(radians);
        return m;
    }
    //Regresa vértices transformados
    //Recibe dos parámetros: los vértices originales y la amtriz de transformación
    public static List<Vector3> ApplyTransform(List<Vector3> originals, Matrix4x4 m)
    {
        List<Vector3> result = new List<Vector3>();

        foreach(Vector3 v in originals)
        {
            Vector4 temp = new Vector4(v.x, v.y, v.z, 1);
            result.Add(m*temp);
        }
        return result;
    }

    public static List<Vector3> DiscriteToContinuous(Vector3 prev, Vector3 next){
        List<Vector3> result = new List<Vector3>();

        Vector3 dir = next - prev;
        float mag = dir.magnitude;
        Vector3 step = dir.normalized;

        for(float i = 0; i < mag; i+=0.1f){
            result.Add(prev + step*i);
        }
        return result;
    }

    public static bool DetectTurn(Vector3 prev, Vector3 next, Vector3 current){
        Vector3 dir = next - prev;
        Vector3 dir2 = current - next;

        float angle = Angle(dir, dir2);
        if(angle > 30){
            return true;
        }
        return false;
    }
    
    public static float Magnitude(Vector3 a){
        return Mathf.Sqrt(a.x * a.x + a.y * a.y + a.z * a.z);
    }

}