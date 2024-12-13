#ifndef EDGE3D_H
#define EDGE3D_H


#include <Eigen/Dense>
#include "SE3.h"


typedef Eigen::MatrixXd Matrix;


class Edge3D{

public:
    Edge3D(){}
    ~Edge3D(){}

    Edge3D(int fromID, int toID, SE3 m, Matrix I){
        this->fromID = fromID;
        this->toID = toID;
        this->m = m;
        this->I = I;
    }

    int getFromID() const {
        return fromID;
    }

    int getToID() const {
        return toID;
    }

    SE3 getM(){
        return m;
    }

    Matrix getI(){
        return I;
    }

    Edge3D getBackwards(){
        return Edge3D(toID, fromID, m.inv(), I);
    }

    double getNoise() {
        double det = I.determinant();
        if (det > 0) {
            return (1.0 / det);
        } else {
            return std::numeric_limits<double>::infinity();
        }
    }

private:
    int toID;
    int fromID;
    SE3 m;
    Matrix I;
};

#endif // EDGE3D_H
