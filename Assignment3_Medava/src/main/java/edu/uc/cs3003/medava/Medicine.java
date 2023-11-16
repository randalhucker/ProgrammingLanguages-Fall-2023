package edu.uc.cs3003.medava;

public abstract class Medicine implements Shippable{
	private String mMedicineName;

	public Medicine(String medicineName) {
		mMedicineName = medicineName;
	}

	public abstract MedicineSchedule getSchedule();

	public String getMedicineName() {
		return mMedicineName;
	}

	public boolean isTemperatureRangeAcceptable(Double lowTemperature, Double highTemperature) {
		if (this.minimumTemperature() <= lowTemperature &&
				highTemperature <= this.maximumTemperature()) {
			return true;
		}
		return false;
	}

	public double minimumTemperature() {
		return 0.0;
	}

	public double maximumTemperature() {
		return 100.0;
	}

}