#pragma once
#include <vector>
#include "Polymer.h"
#include "Vect3d.h"
class Modifier
{
public:
	Modifier(void);
	~Modifier(void);
	virtual void Act(vector<Polymer*> sys, Polymer* yolk) = 0;
};

class PinBackbone : public Modifier
{
public:
	PinBackbone(vector<Polymer*> sys, double initpk, double initsk, double initstiffk, int numpin);
	~PinBackbone(void);
	void Act(vector<Polymer*> sys, Polymer* yolk);

	double pk, sk, stiffk, linksize, basek;
	double mag1, mag2;
	int numpin;
	vect_d f1, f2;
	vector<vect_d> pins;
};

class OseenTensor : public Modifier
{
public:
	OseenTensor(vector<Polymer*>,double);
	~OseenTensor(void);
	void Act(vector<Polymer*> sys, Polymer* yolk);

	vector<Polymer*> tempsys;
	double k, norm, normsq;
	vect_d dif;
	vect_d mirdif, mirVel;
	double mirnorm, mirnormsq, mirnorm4, h, hminusz, mVeldotmDif;
};

class KinesinShift : public Modifier
{
public:
	KinesinShift(double);
	~KinesinShift(void);
	void Act(vector<Polymer*> sys, Polymer* yolk);

	double k;
};
