package com.gaotianpu.ftodo.ui;

import com.gaotianpu.ftodo.MyApplication;
import com.gaotianpu.ftodo.R;
import com.gaotianpu.ftodo.R.layout;
import com.gaotianpu.ftodo.da.UserBean;

import android.app.Activity;
import android.app.Fragment;
import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

public class ItemDetailFragment extends Fragment {

	public static final String SUBJECT_LOCAL_ID = "subject_local_id";

	private Activity act;
	private MyApplication app;
	private UserBean user;

	private Long subject_local_id;

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.fragment_item_detail,
				container, false);

		act = this.getActivity();
		app = (MyApplication) act.getApplicationContext();
		user = app.getUser();

		subject_local_id = getArguments().getLong(SUBJECT_LOCAL_ID);

		//getActivity().setTitle("ItemDetailFragment");
		return rootView;
	}
}